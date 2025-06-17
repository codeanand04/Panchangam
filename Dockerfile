# Start with a clean, official Python 3.11 image
FROM python:3.11-slim-bullseye

# Set environment variables to make Python run smoothly in Docker
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code (app.py) into the container
COPY . .

# Tell Fly.io that the application listens on port 8080
EXPOSE 8080

# The command that will be run to start your Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
