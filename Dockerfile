# Face-Recon Backend – Docker image
#
# Build:  docker build -t face-recon-backend .
# Run:    docker run -p 5000:5000 face-recon-backend

FROM python:3.11-slim

# System libraries required by OpenCV and dlib
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first (layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY src/ ./src/
COPY backend/ ./backend/
COPY docker-entrypoint.sh ./

# Create runtime directories
RUN mkdir -p data/known_faces data/unknown_faces logs \
    && chmod +x docker-entrypoint.sh

# Expose Flask port
EXPOSE 5000

ENTRYPOINT ["./docker-entrypoint.sh"]
