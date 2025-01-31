# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set environment variables to prevent Python from writing pyc files and buffering output
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install the dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project into the container
COPY . /app/

# Expose the port the app will run on
EXPOSE 8000
