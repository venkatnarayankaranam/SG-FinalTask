# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy all files first (including requirements.txt and app.py)
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable
ENV PYTHONPATH=.

# Default command to run the app
CMD ["python", "app/app.py", "3", "4"]