# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set environment variables to non-interactive to avoid prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=app.py

# Define environment variable for RabbitMQ
ENV RABBITMQ_HOST=localhost

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
