# Dockerfile
FROM python:3.11-slim

# Install dependencies
RUN pip install --no-cache-dir flask requests googletrans==4.0.0-rc1

# Application code
WORKDIR /app
COPY todolist.py .
COPY templates/ ./templates/

# Expose the port and start the app
EXPOSE 5002
CMD ["python", "todolist.py"]

