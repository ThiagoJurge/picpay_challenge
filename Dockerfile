# Use Python base image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Set environment variables (Flask)
ENV FLASK_APP=run.py
ENV FLASK_ENV=development

CMD ["flask", "run", "--host=0.0.0.0"]
