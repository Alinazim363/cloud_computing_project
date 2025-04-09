# For syntax details, see https://docs.docker.com/engine/reference/builder/
FROM python:3

# Install Flask and requests modules
RUN pip install flask requests

# Expose port 5000 (Flask will run on this port inside the container)
EXPOSE 5002

# Set the working directory in the container
WORKDIR /app

# Copy your application code into the container. 
# Here, we assume that your main Flask app is in todolist.py.
COPY todolist.py .

# Copy the templates directory (ensure your index.html is inside this folder)
COPY templates/ ./templates/

# Launch the application when the container starts.
CMD ["python", "todolist.py"]
