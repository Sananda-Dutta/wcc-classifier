FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# Install CPU-only torch first (much smaller than the default GPU build,
# which matters for free-tier deploy speed and storage on Railway).
RUN pip install --no-cache-dir torch==2.7.1 --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Railway auto-detects the port via $PORT — fall back to 8000 locally.
ENV PORT=8000
EXPOSE 8000

CMD uvicorn app:app --host 0.0.0.0 --port ${PORT}
