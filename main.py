import cv2
class ArUcoDetector:
    # change DICT_4X4_50 to DICT_6X6_250 for 6x6 markers, or DICT_5X5_100 for 5x5 markers, etc.
    def __init__(self, dictionary=cv2.aruco.DICT_4X4_50):
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(dictionary)
        self.parameters = cv2.aruco.DetectorParameters()
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise Exception("Could not open video device")


    def draw_markers(self, frame, corners, ids):
        if corners is not None and len(corners) > 0:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        return frame
    
    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

        
    # Placeholder for marker processing logic
    # Replace with actual processing code as needed
    def ProcessMarker(self, marker_id):
        
        print(f"Processing marker ID: {marker_id}")
        
    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            corners, ids, rejected = cv2.aruco.detectMarkers(frame, self.aruco_dict, parameters=self.parameters)
            frame = self.draw_markers(frame, corners, ids)

            if ids is not None:
                for i in range(len(ids)):
                    self.ProcessMarker(ids[i][0])
            cv2.imshow('ArUco Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.release()     


def main():
    rm = ArUcoDetector()
    try:
        rm.run()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        rm.release()
    return None

if __name__ == "__main__":
    main()
