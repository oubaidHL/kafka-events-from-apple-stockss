# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the consumer code and requirements.txt into the container
COPY consumer.py requirements.txt /app/

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the consumer script
CMD ["python", "consumer.py"]
