# Use Python base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Expose port 8000
EXPOSE 8000

# Run the Django app
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
