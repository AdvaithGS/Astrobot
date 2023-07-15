FROM python:3.10

# Set the working directory in the container
WORKDIR /astrobot

# Copy the application files into the working directory
COPY requirements.txt .

# Install the application dependencies
RUN pip install -r requirements.txt

COPY ./bot ./bot

CMD ["python", "./bot/main.py"]

#docker build -t astrobot -label astrobot .
#docker run -d --env-file .env astrobot
#docker attach <container id>