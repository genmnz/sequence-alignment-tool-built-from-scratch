"""
Local launcher: starts the server and opens the browser once.

Production hosts never run this file -- they import `app` from wsgi.py.
"""

import os
import threading
import webbrowser

from api import app

PORT = int(os.environ.get("PORT", 8000))
URL = f"http://localhost:{PORT}"


def open_browser():
    webbrowser.open(URL)


if __name__ == "__main__":
    # The reloader runs this module twice; only the child process (or a
    # non-reloading run) should open a tab, otherwise every save spawns one.
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        threading.Timer(1.0, open_browser).start()

    print(f"Serving on {URL}")
    app.run(host="0.0.0.0", port=PORT)
