# backend/Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Copy dependency lists
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend app code
COPY app ./app

# Expose FastAPI port
EXPOSE 8000

# Run server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
