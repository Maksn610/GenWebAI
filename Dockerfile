FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app app
COPY generate.py ./
COPY site_template.html ./app/templates/
COPY logger_config.py ./app/

RUN echo "[]" > logs.json

RUN mkdir -p /app/sites
VOLUME ["/app/sites"]

EXPOSE 8010
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8010"]
