# mods/screenshare.py
import sys
import threading
import time
import socket
from io import BytesIO
from http.server import BaseHTTPRequestHandler, HTTPServer
from PIL import ImageGrab as ig

class ScreenShareServer:
    def __init__(self, port=8000, fps=60, on_ready=None):
        self.port = port
        self.fps = fps
        self.screenbuf = b""
        self.lock = threading.Lock()
        self.running = True
        self.on_ready = on_ready
        self.screenfile = BytesIO()

        
        threading.Thread(target=self.capture_frames, daemon=True).start()
        threading.Thread(target=self.start_server, daemon=True).start()

    def capture_frames(self):
        while self.running:
            try:
                im = ig.grab()
                self.screenfile.seek(0)
                self.screenfile.truncate(0)
                im.convert("RGB").save(self.screenfile, format="JPEG", quality=75, progressive=True)
                with self.lock:
                    self.screenbuf = self.screenfile.getvalue()
            except Exception as e:
                print(f"[Error] capture_frames: {e}", file=sys.stderr)
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
        ip = self.get_local_ip()
        url = f"http://{ip}:{self.port}/screenshare"

        if self.on_ready:
            self.on_ready(url)
        else:
            pass


        class ScreenShareHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path != '/screenshare':
                    self.send_error(404)
                    return

                self.send_response(200)
                self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=frame')
                self.end_headers()

                try:
                    while True:
                        frame = self.server.screen_server.get_frame_bytes()
                        self.wfile.write(b"--frame\r\n")
                        self.send_header('Content-Type', 'image/jpeg')
                        self.send_header('Content-Length', str(len(frame)))
                        self.end_headers()
                        self.wfile.write(frame)
                        self.wfile.write(b'\r\n')
                        time.sleep(1.0 / self.server.screen_server.fps)
                except (BrokenPipeError, ConnectionResetError):
                    pass
                except Exception:
                    pass

            def log_message(self, format, *args):
              
                return


        server = HTTPServer(('', self.port), ScreenShareHandler)
        server.screen_server = self

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.running = False
            server.server_close()
