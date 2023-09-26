FROM python:3.10

FROM postgres:16

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt ./

# Install the required packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Set the environment variables for PostgreSQL
ENV POSTGRES_USER $PG_USER
ENV POSTGRES_PASSWORD $PG_PWD
ENV POSTGRES_DB $PG_DB
ENV PGDATA /var/lib/postgresql/data/pgdata

# Expose the port for the Flask web app
EXPOSE 5000

# Start the Flask web app
CMD ["python3", "app.py"]


