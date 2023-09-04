# Use an official Python runtime as a parent image
FROM continuumio/miniconda3

########### PREPARE EVERYTHING FOR BUILDING #####################

# Install all dependencies
RUN apt-get update
RUN apt-get -y install build-essential
RUN apt-get install -y git python3-dev cmake make gcc g++ libssl-dev

# Set the OpenSSL root directory to the Miniconda environment
ENV OPENSSL_ROOT_DIR=/opt/conda

########################### PREPARED #############################

################# BUILDING PYMGCLIENT ############################

# Create a conda environment
RUN conda create -n bor_env python=3.9.16

# Activate the conda environment
SHELL ["conda", "run", "-n", "bor_env", "/bin/bash", "-c"]

# Clone the mgclient repository
RUN git clone --recurse-submodules https://github.com/memgraph/pymgclient.git

# Change to the repository directory
WORKDIR /pymgclient

# Change flags so warnings aren't treated as errors
ENV CFLAGS=-Wno-error

# Build the thing
RUN python setup.py install

################# BUILDING PYMGCLIENT FINISHED #####################

################# INSTALLING AND RUNNING MAGICGRAPH ################

# Set the working directory inside the container
WORKDIR /usr/src/bor

# Copy the current directory contents into the container at /usr/src/bor
COPY . /usr/src/bor

RUN pip install --upgrade pip
RUN pip install setuptools wheel

# Install the project dependencies
RUN pip install --no-cache-dir -e . -vv

# Needed for nltk to work
RUN python -m nltk.downloader punkt

# Command to run the application
ENTRYPOINT ["conda", \
            "run", \
            "--no-capture-output", \
            "-n", \
            "bor_env", \
            "uvicorn", \
            "core.restapi.api:app", \
            "--host", \
            "0.0.0.0", \
            "--port", \
            "8000"]

################# FINISHED ##########################################