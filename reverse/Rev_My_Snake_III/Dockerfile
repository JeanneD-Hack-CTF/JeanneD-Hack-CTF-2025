FROM python:3.10.14-bullseye

# Update the system, download any packages essential for the challenge
RUN apt-get -y update && apt-get install -y \
    autoconf \
    bison \
    flex \
    gcc \
    g++ \
    git \
    libnl-route-3-dev \
    libtool \
    make \
    pkg-config \
    python3 \
    git \
    build-essential \
    libssl-dev \
    make \
    python3-pip \
    xxd \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install python-config


