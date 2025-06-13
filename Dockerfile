FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY app app
COPY generate.py .
RUN echo "[]" > logs.json


# Create sites folder (for volume mapping)
RUN mkdir sites
VOLUME ["/app/sites"]

# Expose port and run FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8010"]
