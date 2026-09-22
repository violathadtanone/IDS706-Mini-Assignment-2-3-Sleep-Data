FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY Sleep_health_and_lifestyle_dataset.csv .
COPY Testing ./Testing

CMD ["python", "-m", "pytest", "-vv"]