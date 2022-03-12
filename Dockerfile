# This Dockerfile is from https://github.com/thedirtyfew/dash-docker-mwe

FROM python:3.8-slim-buster

# Create a working directory.
RUN mkdir wd
WORKDIR wd

# Install Python dependencies.
COPY requirements.txt .
RUN apt-get update && apt-get install -y gcc
RUN apt-get install -y g++ 
RUN apt-get install -y binutils libproj-dev gdal-bin
RUN apt-get install -y libgdal-dev

RUN pip3 install -r requirements.txt

# Copy the rest of the codebase into the image
COPY src/ ./
COPY data/ ./data/

# Finally, run gunicorn.
CMD [ "gunicorn", "--workers=5", "--threads=1", "-b 0.0.0.0:8000", "app:server"]

