import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import cvzone
from pynput.keyboard import Controller

# Initialize video capture
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Initialize hand detector
detector = HandDetector(detectionCon=0.8)
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
finalText = ""

keyboard = Controller()


# Function to draw buttons on the keyboard
def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (
        button.pos[0], button.pos[1], button.size[0], button.size[1]),
                          20, rt=0)
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255),
                      cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img


# Button class
class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text


# Create a list of buttons
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture image from camera.")
        break

    # Detect hands
    hands, img = detector.findHands(img)

    # Draw keyboard buttons
    img = drawAll(img, buttonList)

    if hands:
        # Extract the landmarks of the first hand
        lmList = hands[0]['lmList']  # List of landmarks
        if lmList:
            for button in buttonList:
                x, y = button.pos
                w, h = button.size

                # Check if the tip of the index finger (landmark 8) is over a button
                if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                    # Highlight the button
                    cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5),
                                  (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                    # Calculate distance between index finger (8) and middle finger (12)
                    result = detector.findDistance((lmList[8][0], lmList[8][1]),
                                                   (lmList[12][0],
                                                    lmList[12][1]))
                    l = result[0]  # Extract the distance value
                    print("Distance:", l)

                    # If distance is small, simulate button click
                    if l < 30:
                        keyboard.press(button.text)
                        cv2.rectangle(img, button.pos, (x + w, y + h),
                                      (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255),
                                    4)
                        finalText += button.text
                        sleep(0.15)

    # Display typed text
    cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 430),
                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    # Show the image
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
