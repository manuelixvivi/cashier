FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y     gcc     libpq-dev     && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Run with gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:application"]
