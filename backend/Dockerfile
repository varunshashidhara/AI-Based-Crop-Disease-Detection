FROM python:3.10-slim

WORKDIR /code

# Install system dependencies required by OpenCV/TensorFlow/PIL if needed
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir pydantic-settings

COPY app /code/app

# We don't necessarily want to copy the Data directory or scripts if deploying
# Add .dockerignore if necessary to exclude heavy folders not needed in prod

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
