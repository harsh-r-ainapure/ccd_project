FROM python:3.12-slim

WORKDIR /app

COPY app.py .
COPY index.html .

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["python", "app.py"]