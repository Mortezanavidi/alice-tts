# Use Python 3.10 as the base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the main.py
COPY main.py .

# Copy the requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app will run on
EXPOSE 5500

# Run the application (adjust if your entry point is different)
CMD ["python", "main.py"]