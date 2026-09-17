#Import python3
FROM python:3.12-slim

#Create a container directory
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure a real (empty) database.db file exists in the image before the
# docker-compose volume attaches to it. Without this, Docker creates a
# DIRECTORY at this path instead of a file when the named volume mounts,
# and sqlite3.connect() fails with "unable to open database file".
RUN touch database.db

EXPOSE  8000

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]