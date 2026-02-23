# Backend + Frontend simple multi-stage build
# Stage 1: build frontend
FROM node:20 AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json frontend/pnpm-lock.yaml* ./
COPY frontend/ .
RUN npm install
RUN npm run build

# Stage 2: backend image
FROM python:3.11-slim
WORKDIR /app
# system deps for pillow/playwright
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libjpeg-dev libpng-dev curl ca-certificates && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend and built frontend
COPY backend/ ./backend/
COPY --from=frontend-build /app/frontend/dist ./frontend_dist

EXPOSE 5000
ENV FLASK_APP=backend/app.py
CMD ["python", "backend/app.py"]