import subprocess
import time

def open_locked_chrome():
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Update if needed
    url = "http://127.0.0.1:8000/alert"

    chrome_cmd = [
        chrome_path,
        "--kiosk",
        "--disable-infobars",
        "--disable-session-crashed-bubble",
        "--disable-popup-blocking",
        "--noerrdialogs",
        "--incognito",
        url
    ]

    process = subprocess.Popen(chrome_cmd)
    process.wait()
    time.sleep(5)
    

