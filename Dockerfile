FROM python:3.11-slim

# Install Flask and requests modules
RUN pip install flask requests googletrans==4.0.0-rc1

# Expose port 5002 
EXPOSE 5002

# Set the working directory in the container
WORKDIR /app

# Copy your application code into the container. 
COPY todolist.py .

# Copy the templates directory 
COPY templates/ ./templates/

# Launch the application when the container starts.
CMD ["python", "todolist.py"]
