# Use an official Python runtime as a parent image
# Use alpine with Python pre-installed
FROM python:3.9-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Add essential packages and psycopg2 prerequisites then upgrade pip
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev postgresql-dev \
    && pip install --upgrade pip

# Install python packages and remove unnecessary packages
RUN pip install --no-cache-dir -r requirements.txt \
    && apk del build-deps

# Copy the rest of the application code
COPY insight /app/insight

# Env Variables
ENV APP_PORT=3000

# Run the command to start uWSGI
CMD uvicorn insight.main:app --host 0.0.0.0 --port $APP_PORT

# Expose APP_PORT of the container to the outside
EXPOSE $APP_PORT