FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the Flask app to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask will run on
EXPOSE 80

# Start the Flask app
CMD ["python", "app.py"]
