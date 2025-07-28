FROM python:3.10-slim

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the App code and input/output folders
COPY App/ App/
COPY input/ input/
COPY output/ output/

# Run the main script
CMD ["python", "App/main.py"]
