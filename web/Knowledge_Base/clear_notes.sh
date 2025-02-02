#!/bin/bash

# UUIDv4 regex pattern
PATTERN=".*/[0-9a-f]\{8\}-[0-9a-f]\{4\}-[0-9a-f]\{4\}-[0-9a-f]\{4\}-[0-9a-f]\{12\}"

# Find all user folders and remove those older than 1 hour
find ./app/notes -type d -regex "${PATTERN}" -atime +1h -print -exec rm -r {} +
