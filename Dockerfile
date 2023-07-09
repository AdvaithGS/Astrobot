FROM python:3.10

# Set the working directory in the container
WORKDIR ./

# Copy the application files into the working directory
COPY . ./astrobot

# Install the application dependencies
RUN pip install -r astrobot/requirements.txt
RUN cd astrobot

CMD ["python", "bot/main.py"]