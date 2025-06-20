FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y libjpeg-dev zlib1g-dev && \
    pip install -r requirements.txt
CMD ["python", "app.py"]
