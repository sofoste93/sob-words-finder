"""Desktop launcher used by the packaged executable."""

import threading
import webbrowser

from waitress import serve

from app import app

if __name__ == "__main__":
    url = "http://127.0.0.1:8765"
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    serve(app, host="127.0.0.1", port=8765, threads=4)
