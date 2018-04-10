__author__ = 'Usama Sarwar'
# !/bin/env python

# python version 3.4.3
import os
import cv2   # Open cv2 - 3.1.0 version
import pyautogui


# Required Parameters for the camera access and calculating distcances for tracking
HAAR_CASCADE_PATH = "haarcascade_frontalface_alt.xml"
camera_fps = 20
horizontal_tolerance = 15.0
upward_tolerance = 15.0
downward_tolerance = -15.0



# Function to detect faces
def detect_faces(image):
    faces = []
  #  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    detected = face_cascade.detectMultiScale(
        image,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    if detected != []:
        for (x, y, w, h) in detected:  # for (x,y,w,h),n in detected:
            faces.append((x, y, w, h))
    return faces

# Function that gets motion: Horizontal [Left, Right] and  Vertical [Up and down]
def record_head_motion(faceCenter, originCenter):
    # [0][0] - x, [0][1] - y, [0][2] - w, [0][3] - h
    horizontal_change = faceCenter[0] - originCenter[0]
    vertical_change = faceCenter[1] - originCenter[1]

    ver = vertical_change < upward_tolerance and vertical_change > downward_tolerance
    if abs(horizontal_change) < horizontal_tolerance and ver:
        print('ORIGIN', horizontal_change, vertical_change)
        return 25, 0
    if vertical_change >= 0:
        if abs(horizontal_change) > (horizontal_tolerance // abs(downward_tolerance)) * abs(
                vertical_change):
            if horizontal_change > 0:
                print('LEFT', horizontal_change, vertical_change)
                return 2, horizontal_change
            else:
                print('RIGHT', horizontal_change, vertical_change)
                return 1, -horizontal_change
        else:
            print('DOWN', horizontal_change, vertical_change)
            return 3, vertical_change

    if vertical_change < 0:
        if abs(horizontal_change) > (horizontal_tolerance // abs(upward_tolerance)) * abs(
                vertical_change):
            if horizontal_change > 0:
                print('LEFT', horizontal_change, vertical_change)
                return 2, horizontal_change
            else:
                print('RIGHT', horizontal_change, vertical_change)
                return 1, -horizontal_change
        else:
            print('UP', horizontal_change, vertical_change)
            return 4, vertical_change
    print(horizontal_change, vertical_change)


#Driver Program
def run_driver_program():

    originCenter = None
    faceArray = []
    faceCenter = None
    i = 0
    while True:
        retval, image = capture.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Video", image)
        # Only run the Detection algorithm every 3 frames to improve performance

        if i % 3 == 0:
            faces = detect_faces(gray)
        if faces:
            faceCenter = (faces[0][0] + faces[0][2] // 2, faces[0][1] + faces[0][3] // 2)
            print('current coordinates: ', faces)

        if faceCenter:
            faceArray.append(faceCenter)

        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), 255)
            cv2.rectangle(image, (faceCenter[0] - 1, faceCenter[1] - 1), (faceCenter[0] + 1, faceCenter[1] + 1), 255)
        if originCenter:
            cv2.rectangle(image, (originCenter[0] - 1, originCenter[1] - 1), (originCenter[0] + 1, originCenter[1] + 1),
                          0)

        if originCenter and faceCenter and faceCenter != []:
            direction, val = record_head_motion(faceCenter, originCenter)
            if direction in key_to_function:
                key_to_function[direction]() # Calling function to press keyboard through head movement through pyautoguiv library.

        if i % 20 == 0 and faces:
            # approx 3 secs of config time
            faceCenter_avg_y = sum([j[1] for j in faceArray]) // len(faceArray)
            faceCenter_avg_x = sum([j[0] for j in faceArray]) // len(faceArray)
            originCenter = [faceCenter_avg_x, faceCenter_avg_y]
            faceArray = []
            print('origin of face is:  ', originCenter)


    if not faces:
        i -= 1
        i += 1
        c = cv2.waitKey(0)
        if c == 27:
            return


# Controller for Moving paddle/Cursor in all 4 directions as per detected motion
def moveRight():
    pyautogui.press('right')


def moveLeft():
    pyautogui.press('left')


def moveUp():
    pyautogui.press('up')


def moveDown():
    pyautogui.press('down')

# making sure functions get their respective names and run on main
if __name__ == '__main__':
    key_to_function = {
        1: moveRight,
        2: moveLeft,
        3: moveDown,
        4: moveUp,
    }

cv2.namedWindow("Camera", 640)
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FPS, 30)
face_cascade = cv2.CascadeClassifier(HAAR_CASCADE_PATH)

# os.system("google-chrome --new-window index.html")
run_driver_program()
capture.release()
cv2.destroyAllWindows()

