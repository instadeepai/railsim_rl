
# Use a base image with CUDA installed
FROM nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04

# Install wget and other necessary tools
RUN apt-get update && \
    apt-get install -y wget gnupg && \
    apt-get clean;

# # Add Amazon Corretto repository
# RUN wget -O- https://apt.corretto.aws/corretto.key | apt-key add - && \
#     add-apt-repository 'deb https://apt.corretto.aws stable main' && \
#     apt-get update

# # Install Amazon Corretto 21
# RUN apt-get install -y java-21-amazon-corretto-jdk && \
#     apt-get clean;


RUN apt-get update
RUN apt-get -y install openjdk-21-jdk


# Install Python and pip
RUN apt-get -y install python3 python3-pip
ENV PATH="/usr/bin:$PATH"

# Set up environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-1.21.0-amazon-corretto
ENV PATH="$JAVA_HOME/bin:${PATH}"

# Set the working directory inside the container
WORKDIR /app

# # Copy the Java project files to the container
COPY requirements.txt ./

# Add python and pip binaries to the PATH variable
ENV PATH="/usr/bin:$PATH"

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt