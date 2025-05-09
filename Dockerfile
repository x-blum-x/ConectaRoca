FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/db && chmod -R 777 /app/db

COPY . .

EXPOSE 5000
CMD ["python", "app/app.py"]
