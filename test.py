import cv2
# Load ArUco dictionary and detector parameters
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()

# Initialize webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

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
