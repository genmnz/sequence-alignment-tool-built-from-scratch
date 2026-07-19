"""
WSGI entrypoint. Used by gunicorn (`gunicorn wsgi:app`) and picked up
automatically by hosts that look for a WSGI `app` (Vercel, Passenger, uWSGI).
"""

from api import app

__all__ = ["app"]
