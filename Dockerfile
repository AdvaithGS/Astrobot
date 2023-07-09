FROM python:3.10

# Set the working directory in the container
WORKDIR ./

# Copy the application files into the working directory
COPY . ./Astrobot

# Install the application dependencies
RUN ls bot
RUN pwd
RUN pip install -r Astrobot/requirements.txt

CMD ["python", "bot/main.py"]