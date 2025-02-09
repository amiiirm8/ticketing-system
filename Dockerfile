# Use the official Python image as the base image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the working directory
COPY . .

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# Expose the port the Django app runs on
EXPOSE 8000

# Set the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ticketing_system.wsgi:application"]
