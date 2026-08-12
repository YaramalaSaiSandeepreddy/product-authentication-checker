# Optional Docker deployment for the full application.
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends     gcc libjpeg-dev libpng-dev curl ca-certificates     && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt
RUN playwright install --with-deps chromium

COPY backend/ ./backend/
COPY frontend/ ./frontend/

EXPOSE 5000
ENV PYTHONUNBUFFERED=1
CMD ["gunicorn", "--chdir", "backend", "app:app"]
