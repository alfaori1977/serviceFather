# Use an official Python runtime as a parent image
FROM python:3.8-slim
RUN apt-get install screen

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./src /app

# Install any needed packages specified in requirements.txt
RUN pip install Flask
RUN pip install Flask-Cors
RUN pip install python-dotenv
RUN pip install pyopenssl
# Make port 16000 available to the world outside this container
EXPOSE 16000

# Define environment variable
ENV SERVICE_FATHER_TOKEN_ID ""

# Run app.py when the container launches
CMD ["python", "httpServer.py"]
