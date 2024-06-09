# Use an official Ubuntu base image
FROM ubuntu:20.04

# Set environment variables to non-interactive to avoid prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages
RUN apt-get update
RUN apt-get install -y \
    git \
    make \
    gcc  \
    pkg-config \
    libcap-dev \
    asciidoc \
    python3 \
    python3-pip \
    && apt-get clean
RUN apt-get install -y  libsystemd-dev
# Clone the IOI/Isolate repository
RUN git clone https://github.com/ioi/isolate.git /opt/isolate

# Build and install Isolate
RUN cd /opt/isolate && make && make install

# Set up isolate directory
RUN mkdir -p /var/lib/isolate

# Set the working directory
# WORKDIR /opt/isolate

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

EXPOSE 5672

# Display isolate version to verify installation
CMD ["python3", "worker.py"]
