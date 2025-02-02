#!/bin/bash

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

# Only build the challenge if it does not already exists (as it's quite long to build)
if [ ! -f "$SCRIPT_DIR/next_level" ]; then
  $SCRIPT_DIR/../docker/build.sh
  docker run -it -v "$SCRIPT_DIR":/home docker_compiler:latest make -C /home
fi
