FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask gunicorn requests beautifulsoup4

COPY app.py /app/

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
