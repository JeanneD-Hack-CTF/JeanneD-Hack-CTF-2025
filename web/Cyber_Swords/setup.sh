#!/bin/bash

# Function to display help message
display_help() {
    echo "Usage: deploy.sh [OPTIONS]"
    echo "Options:"
    echo "  -r, --rebuild     Rebuild the Docker image"
    echo "  -h, --help        Display this help message"
    echo "  -d, --down        Tear down the deployment"
}

# Function to rebuild the Docker image
rebuild_image() {
    docker build -t jwt_mania_1 .
}

# Function to tear down the deployment
tear_down() {
    docker stop jwt_mania_1
    docker rm jwt_mania_1
}

# Parse command line options
while [[ $# -gt 0 ]]; do
    case $1 in
        -r|--rebuild)
            rebuild_image
            shift
            ;;
        -h|--help)
            display_help
            exit 0
            ;;
        -d|--down)
            tear_down
            exit 0
            ;;
        -s|--shell)
            docker exec -it jwt_mania_1 /bin/bash
            exit 0
            ;;
        *)
            echo "Invalid option: $1"
            display_help
            exit 1
            ;;
    esac
done

# Default behavior: build and run the Docker container
rebuild_image
docker run -d -p 8087:80 --name jwt_mania_1 jwt_mania_1

# chown for the script
# chmod +x setup.sh