FROM ubuntu:18.04

# Update the system, download any packages essential for the challenge
RUN dpkg --add-architecture i386
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
    gcc \
    gcc-multilib \
    libc6:i386 \
    libstdc++6:i386 \
    libseccomp2:i386 \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/google/nsjail /nsjail
RUN cd /nsjail && make && mv /nsjail/nsjail /bin && rm -rf -- /nsjail

# RUN mkdir /jail
WORKDIR /app
COPY makefile . 
COPY special_value.c .
COPY flag.txt .

RUN make && ls -lisa /app/ && echo "Compilation Done" 
RUN chmod +x /app/special_value && ls -lisa /app/special_value
RUN chmod -R 755 .

CMD nsjail \
  -Ml --port 9000 \
  --user nobody \
  --group nogroup \
  -R /app/flag.txt \
  -R /app/special_value \
  -R /lib -R /lib64 -R /usr/lib -R /usr/local/lib \
  --chroot /app \
  -- /app/special_value 
