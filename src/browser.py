import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt, pyqtSignal, QObject, pyqtSlot, QTimer


# Define a communicator with signals for opening and closing.
class Communicator(QObject):
    open_signal = pyqtSignal()
    close_signal = pyqtSignal()

communicator = Communicator()

class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lockdown Browser")
        screen_size = QApplication.primaryScreen().size()
        self.setGeometry(0, 0, screen_size.width(), screen_size.height())

        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # Create WebView and load Flask app
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://127.0.0.1:8000"))

        # Disable context menu (right-click)
        self.browser.setContextMenuPolicy(0)

        # Set layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        communicator.open_signal.connect(self.seizure)
        communicator.close_signal.connect(self.end_seizure)

        self.cooldown = False

    @pyqtSlot()
    def seizure(self):
        if self.cooldown:
            print("Cooldown active: seizure() call ignored.")
            return
        print("seizure in browser")
        self.browser.setUrl(QUrl("http://127.0.0.1:8000/alert"))
        self.show()

    @pyqtSlot()
    def end_seizure(self):
        self.browser.setUrl(QUrl("http://127.0.0.1:8000"))
        self.hide()
        self.cooldown = True
        QTimer.singleShot(3000, self.reset_cooldown)

    def reset_cooldown(self):
        self.cooldown = False
        print("Cooldown ended: seizure() is active again.")


def open_browser():
    app = QApplication(sys.argv)
    window = SimpleBrowser()
    # window.show()
    # window.hide()
    app.exec_()