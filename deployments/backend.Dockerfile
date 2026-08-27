FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt black ruff

COPY backend /app/backend
WORKDIR /app/backend

RUN addgroup --system echomart && \
    adduser --system --ingroup echomart echomart && \
    chown -R echomart:echomart /app

USER echomart

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
