#mods/screenshare.py
import sys
import threading
import time
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer

ver = sys.version_info.major
if ver == 2:
    import StringIO as io
elif ver == 3:
    import io

if sys.platform in ["win32", "darwin"]:
    from PIL import ImageGrab as ig
else:
    import pyscreenshot as ig
    bkend = "pygdk3"


class ScreenShareServer:
    def __init__(self, port=8000, fps=60):
        self.port = port
        self.fps = fps
        self.ver = ver
        self.screenbuf = b""
        self.lock = threading.Lock()
        self.running = True

        if self.ver == 2:
            self.screenfile = io.StringIO()
        else:
            self.screenfile = io.BytesIO()

        threading.Thread(target=self.capture_frames, daemon=True).start()

    def __del__(self):
        self.screenfile.close()

    def capture_frames(self):
        while self.running:
            if sys.platform in ["win32", "darwin"]:
                im = ig.grab()
            else:
                im = ig.grab(childprocess=False, backend=bkend)

            self.screenfile.seek(0)
            self.screenfile.truncate(0)
            im_converted = im.convert("RGB")
            im_converted.save(self.screenfile, format="jpeg", quality=75, progressive=True)
            with self.lock:
                self.screenbuf = self.screenfile.getvalue()
            time.sleep(1.0 / self.fps)

    def get_frame_bytes(self):
        with self.lock:
            return self.screenbuf

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def start_server(self):
        class Handler(BaseHTTPRequestHandler):
            def do_GET(handler_self):
                if handler_self.path != '/screenshare':
                    handler_self.send_error(404)
                    return

                handler_self.send_response(200)
                handler_self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=frame')
                handler_self.end_headers()

                try:
                    while True:
                        frame = self.get_frame_bytes()
                        handler_self.wfile.write(b"--frame\r\n")
                        handler_self.send_header('Content-Type', 'image/jpeg')
                        handler_self.send_header('Content-Length', str(len(frame)))
                        handler_self.end_headers()
                        handler_self.wfile.write(frame)
                        handler_self.wfile.write(b'\r\n')
                        time.sleep(1.0 / self.fps)
                except Exception as e:
                    print("Client disconnected:", e)

        ip = self.get_local_ip()
        print(f"Starting screen share server at http://{ip}:{self.port}/screenshare")
        print("Open the URL in your browser to view the live screen stream.\nPress Ctrl+C to stop.")

        server = HTTPServer(('', self.port), Handler)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
        finally:
            server.server_close()
            self.running = False



