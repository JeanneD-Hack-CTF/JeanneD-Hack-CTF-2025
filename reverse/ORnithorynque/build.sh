#!/bin/bash

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

$SCRIPT_DIR/../docker/build.sh
docker run -it -v "$SCRIPT_DIR":/home docker_compiler:latest make -C /home
