import cv2
import numpy as np
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
    # This is a color detection function for traffic lights
    def detect_traffic_light_color(self,frame):
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
