# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the csv directory into the container
COPY ./csv /app/csv

# Install the dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 (default port for Flask)
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]
