# Use Python 3.10 base image
FROM python:3.10-slim

# Working Directory inside container
WORKDIR /app

# Copy requirements
COPY src/api/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy model and source
COPY model/model.joblib . 
COPY src/api/v2/main.py .

# Start FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]