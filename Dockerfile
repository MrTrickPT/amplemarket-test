# Use the official Python image
FROM python:3.9-buster

# Set the working directory
WORKDIR /app

# Install Python dependencies
RUN python -m venv .venv && \
    . .venv/bin/activate && \
    pip install --upgrade pip

COPY . .

RUN pip install -r requirements.txt

# Expose port 5001
EXPOSE 5001

# Specify the command to run your application
CMD ["python", "src/api.py"]
