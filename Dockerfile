FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt ./

# Install the required packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose the port for the Flask web app
EXPOSE 5000

# Start the Flask web app
CMD ["python3", "app.py"]





