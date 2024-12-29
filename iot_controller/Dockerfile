FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt --upgrade

COPY app.py app.py
EXPOSE 5000
CMD ["hypercorn", "app:app", "--bind", "0.0.0.0:5000", "--worker-class", "asyncio","--reload"]
