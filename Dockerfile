# Use the official Python image from the Docker Hub
FROM python:3.9-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies from the requirements.txt file
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application files into the container
COPY . .

# Set Flask environment variables for running on 0.0.0.0 (for Docker container)
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Expose port 5000 (default port for Flask)
EXPOSE 5000

# Start the Flask application using flask run
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
