FROM python:3.10

# Set the working directory in the container
WORKDIR ./

# Copy the application files into the working directory
COPY . /bot

# Install the application dependencies
RUN pip install -r requirements.txt

CMD ["python", "bot/main.py"]