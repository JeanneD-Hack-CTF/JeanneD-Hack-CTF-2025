FROM ubuntu:18.04

# Update the system, download any packages essential for the challenge
RUN apt-get -y update && apt-get install -y \
    autoconf \
    bison \
    flex \
    gcc \
    g++ \
    git \
    libprotobuf-dev \
    libnl-route-3-dev \
    libtool \
    make \
    pkg-config \
    protobuf-compiler \
    python3 \
    git \
    build-essential \
    make \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/google/nsjail /nsjail
RUN cd /nsjail && make && mv /nsjail/nsjail /bin && rm -rf -- /nsjail

# RUN mkdir /jail
WORKDIR /app
COPY makefile . 
COPY fear_my_thoughts.c .
COPY flag.txt .

RUN make && ls -lisa /app/ && echo "Compilation Done" 

CMD nsjail \
  -Ml --port 9000 \
  --user nobody \
  --group nogroup \
  -R /dev/urandom \
  -R /app/flag.txt \
  -R /app/fear_my_thoughts \
  -R /lib -R /lib64 -R /usr/lib -R /usr/local/lib \
  --chroot /app \
  -- /app/fear_my_thoughts
