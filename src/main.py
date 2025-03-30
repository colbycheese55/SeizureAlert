import browser
import screenCapture
from ui import app
import threading
from config import config_instance


# def handle_seizure_signal():
#     while True:
#         seizure.wait()
#         browser.open_browser()
#         seizure_end.wait()
#         browser.close_browser()
#         seizure_end.clear()
#         seizure.clear()

if config_instance.get_config_value('enable screen capture'):
    screen_capture_thread = threading.Thread(target=screenCapture.run)
    screen_capture_thread.start()
    print("Screen capture thread started.")

# browser_thread = threading.Thread(target=handle_seizure_signal)
# browser_thread.start()

def run_flask_app():
    app.run(host='127.0.0.1', port=8000, debug=True, use_reloader=False)

flask_thread = threading.Thread(target=run_flask_app)
flask_thread.start()

browser.open_browser()
