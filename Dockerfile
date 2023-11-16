# Use an official Python runtime as the base image
FROM python:3.9
LABEL maintainer="Rishabh"

ENV PYTHONUNBUFFERED 1 
# Create the /app directory and set it as the working directory
RUN mkdir /app
WORKDIR /app

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Create and activate a virtual environment
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all other application files to the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Run Flask database migrations during the Docker image build
# Check conditions for migrations and instance folders
RUN if [ ! -d instance ] && [ ! -d migrations ]; then flask db init; \
    elif [ ! -d instance ] || [ ! -d migrations ]; then rm -rf instance migrations && flask db init && flask db migrate && flask db upgrade; \
    fi

RUN flask db migrate && flask db upgrade

# Run pytest for testing
RUN pytest test.py

# Run the Flask application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:create_app()"]
