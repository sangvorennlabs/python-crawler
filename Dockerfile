# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the entire current directory to the container
COPY . .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and its browsers
RUN playwright install

# Expose the port
EXPOSE 8000

# Start the FastAPI server
CMD ["python", "app.py"]