# FROM --platform=linux/amd64 python:3.10

# # Set working directory
# WORKDIR /app

# # Copy requirements.txt to the container
# COPY requirements.txt .

# # Install dependencies listed in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the processing script (and any additional source code)
# COPY process_pdfs.py .

# # Run the script
# CMD ["python", "process_pdfs.py"]
FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "process_pdfs.py"]
