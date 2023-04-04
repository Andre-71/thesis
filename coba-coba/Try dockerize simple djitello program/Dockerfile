# Use the official image as a parent image
FROM ubuntu:latest

# Ref: https://rtfm.co.ua/en/docker-configure-tzdata-and-timezone-during-build/
ENV TZ=Asia/Jakarta
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Set the working directory
WORKDIR /usr/src/app

# Install any needed packages specified in requirements.txt
RUN apt-get update

RUN apt-get install -y python3 \
    python-pip \
    libsm6 \
    libxext6 \
    libxrender-dev

RUN pip install --upgrade djitellopy

COPY . .

CMD ["python", "main.py"]
