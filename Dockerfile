FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && addgroup --system app \
    && adduser --system --ingroup app app

COPY --chown=app:app . .
USER app

EXPOSE 8000

CMD ["sh", "-c", "python init_db.py && exec gunicorn --bind 0.0.0.0:8000 app:app"]
