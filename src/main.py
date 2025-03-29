import browser
import screenCapture
from ui import app, seizure
import threading


def handle_seizure_signal():
    while True:
        seizure.wait()
        browser.open_browser()
        seizure.clear()

screen_capture_thread = threading.Thread(target=screenCapture.run)
screen_capture_thread.start()

browser_thread = threading.Thread(target=handle_seizure_signal)
browser_thread.start()

app.run(host='127.0.0.1', port=8000, debug=True, use_reloader=False)
