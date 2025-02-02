#!/bin/bash

# Function to display help message
display_help() {
    echo "Usage: deploy.sh [OPTIONS]"
    echo "Options:"
    echo "  -r, --rebuild     Rebuild the Docker image"
    echo "  -h, --help        Display this help message"
    echo "  -d, --down        Tear down the deployment"
    echo "  -s, --shell       Start a shell in the Docker container"
}

# Function to rebuild the Docker image
rebuild_image() {
    docker build -t web_intro .
}

# Function to tear down the deployment
tear_down() {
    docker stop web_intro
    docker rm web_intro
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
            docker exec -it web_intro /bin/bash
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
docker run -d -p 8888:80 --name web_intro web_intro

# chown for the script
# chmod +x setup.sh