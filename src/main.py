import browser
import webcam
import data_processing
import screenCapture
from ui import app, seizure
import threading
from config import read_in_config, get_config_value
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap
import sys
from webcam import SeizureAlertApp


def handle_seizure_signal():
    while True:
        seizure.wait()
        browser.open_browser()
        seizure.clear()

read_in_config()

if get_config_value('enable_screen_capture'):
    screen_capture_thread = threading.Thread(target=screenCapture.run)
    screen_capture_thread.start()
    print("Screen capture thread started.")

if get_config_value('enable_webcam_capture'):
    print("Webcam capture started")
    
    # Ensure QApplication is created in the main thread
    app = QApplication(sys.argv)
    
    # Create the window or the worker thread
    window = SeizureAlertApp()
    window.show()
    
    # Start the webcam capture in a separate thread
    webcam_thread = threading.Thread(target=window.start_webcam)
    webcam_thread.start()
    
    sys.exit(app.exec_())  # Start the Qt event loop

browser_thread = threading.Thread(target=handle_seizure_signal)
browser_thread.start()

app.run(host='127.0.0.1', port=8000, debug=True, use_reloader=False)
