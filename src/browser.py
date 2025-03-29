import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lockdown Browser")
        self.setGeometry(100, 100, 1024, 768)  # Window size

        # Create WebView and load Flask app
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://127.0.0.1:8000/alert"))

        # Disable context menu (right-click)
        self.browser.setContextMenuPolicy(0)

        # Set layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


def open_browser():
    app = QApplication(sys.argv)
    window = SimpleBrowser()
    window.show()
    app.exec_()
