# Builder stage
FROM python:3.12-alpine AS builder
RUN apk add --no-cache build-base gcc libffi-dev musl-dev openssl-dev zlib-dev jpeg-dev postgresql-dev
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/
ENV UV_SYSTEM_PYTHON=1

WORKDIR /app
COPY requirements.txt .
ARG DEV=false
COPY requirements.dev.txt /app/requirements.dev.txt
RUN uv pip install --no-cache-dir -r requirements.txt && \
    if [ "$DEV" = "true" ]; then uv pip install --no-cache-dir -r requirements.dev.txt; fi

# Final stage
FROM python:3.12-alpine
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TZ=Asia/Dhaka

RUN apk add --no-cache tzdata postgresql-client jpeg && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    adduser -D -H -s /bin/false django-user && \
    mkdir -p /vol/web/media /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --chown=django-user:django-user ./app /app

WORKDIR /app
EXPOSE 8000

USER django-user
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "your_project.wsgi:application"]