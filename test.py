import cv2
import numpy as np


# Load ArUco dictionary and detector parameters change 4x4 to 6x6 for 6x6 markers, or 5x5 for 5x5 markers, etc.
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()

# Initialize webcam you can change the 0 to chenge whitch camera you use
cap = cv2.VideoCapture(0)

def detect_traffic_light_color(frame):

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    red_lower1 = np.array([0, 100, 100])
    red_upper1 = np.array([10, 255, 255])
    red_lower2 = np.array([160, 100, 100])
    red_upper2 = np.array([179, 255, 255])

    green_lower = np.array([40, 50, 50])
    green_upper = np.array([80, 255, 255])

    red_mask1 = cv2.inRange(hsv, red_lower1, red_upper1)
    red_mask2 = cv2.inRange(hsv, red_lower2, red_upper2)
    red_mask = cv2.bitwise_or(red_mask1, red_mask2)

    green_mask = cv2.inRange(hsv, green_lower, green_upper)

    kernel = np.ones((5, 5), np.uint8)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)

    red_pixels = cv2.countNonZero(red_mask)
    green_pixels = cv2.countNonZero(green_mask)

    threshold = 500

    if red_pixels > green_pixels and red_pixels > threshold:
        return "Red"
    elif green_pixels > red_pixels and green_pixels > threshold:
        return "Green"
    else:
        return "None"

while True:
    ret, frame = cap.read()
    if not ret:
        break
    color = detect_traffic_light_color(frame)
    print("Detected Traffic Light:", color)

    # Detect markers
    corners, ids, rejected = cv2.aruco.detectMarkers(frame, aruco_dict, parameters=parameters)
    # Draw markers
    if ids is not None:
        for i in range(len(ids)):
            cv2.aruco.drawDetectedMarkers(frame, corners)
            print(f"Detected marker ID: {ids[i][0]}")

    cv2.imshow('ArUco Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
