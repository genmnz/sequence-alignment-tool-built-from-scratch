FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY alignment_logic.py api.py wsgi.py ./
COPY static ./static

ENV PORT=8000
EXPOSE 8000

CMD gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 wsgi:app
