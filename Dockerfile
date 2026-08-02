FROM python:3.12-slim

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/app.py .

EXPOSE 5000

ENV APP_VERSION=1.0.0

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--access-logfile", "-", "--error-logfile", "-", "app:app"]

#CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]#
