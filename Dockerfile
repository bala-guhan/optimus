FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY agent/agent/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy agent code and demo codebase
COPY agent/agent/ ./

# Default command (can be overridden)
CMD ["python", "optimus_prime.py"]