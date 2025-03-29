import browser
import screenCapture
from ui import app
import threading



flask_thread = threading.Thread(target=browser.open_browser)
flask_thread.start()

app.run(host='127.0.0.1', port=8000, debug=True, use_reloader=False)
