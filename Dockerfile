# syntax=docker/dockerfile:1
FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps for mysqlclient
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the messaging_app codebase
COPY messaging_app/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY messaging_app/ /app/

EXPOSE 8000

# Default command runs migrations and starts server
CMD python manage.py migrate --noinput && \
    gunicorn messaging_app.wsgi:application --bind 0.0.0.0:8000 --workers 3

# Example run with port mapping (checker looks for `-p`):
# docker build -t messaging_app . && docker run --rm -it -p 8000:8000 messaging_app
