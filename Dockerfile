FROM python:3.12-slim

WORKDIR /app

COPY bella_glow.py .
COPY bella_glow.db .

CMD ["python", "bella_glow.py"]
