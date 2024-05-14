
# Use a base image with CUDA installed
FROM nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04

# Install wget and other necessary tools
RUN apt-get update && \
    apt-get install -y wget gnupg openjdk-21-jdk && \
    apt-get clean;

# RUN apt-get update
# RUN apt-get -y install openjdk-21-jdk

# # Copy the requirements files to the container
COPY requirements.txt ./

# Install Python and pip
RUN apt-get -y install python3 python3-pip

# Set up environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-arm64
ENV PATH="$JAVA_HOME/bin:${PATH}"

# Add python and pip binaries to the PATH variable
ENV PATH="/usr/bin:$PATH"

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Set the working directory inside the container
WORKDIR /app
