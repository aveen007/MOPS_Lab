FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY simulator.py ./simulator.py

RUN pip install requests

CMD ["python", "simulator.py"]
