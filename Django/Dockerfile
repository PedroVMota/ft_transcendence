FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Set work directory
WORKDIR /code

# Install dependencies
RUN ls
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


EXPOSE 8000
# Copy project
COPY . /code/