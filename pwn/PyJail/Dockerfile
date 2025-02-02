FROM ubuntu:18.04

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
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/google/nsjail /nsjail
RUN cd /nsjail && make && mv /nsjail/nsjail /bin && rm -rf -- /nsjail

# RUN mkdir /jail
WORKDIR /app
COPY jail.py .
COPY flag.txt .

CMD nsjail \
  -Ml --port 9000 \
  --user nobody \
  --group nogroup \
  -R /app/flag.txt \
  -R /app/jail.py \
  -R /bin/sh \
  -R /bin/ls \
  -R /bin/pwd \
  -R /bin/cat \
  -R /lib -R /lib64 -R /usr/lib -R /usr/local/lib -R /usr/lib/python3.6 \
  -R /usr/bin/python3 -R /usr/bin/python3.6 \
  --chroot /app \
  -- /usr/bin/python3 /app/jail.py 
