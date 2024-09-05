# Use a base image with Python
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install huggingface_hub

# Copy the source code
COPY src/ ./src

# Entrypoint for training
CMD ["python", "./src/train.py"]
