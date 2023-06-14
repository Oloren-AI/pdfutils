# Makefile for chemblextension project

# Variables
EXTENSION_NAME = "pdfutils"
DOCKER_IMAGE = ${EXTENSION_NAME}:latest
PORT = 8074

# Phony targets
.PHONY: docker docker-build docker-run

# Default target
all: docker

# Docker target: build and run Docker image
docker: docker-build docker-run

# Docker build target: builds Docker image
docker-build:
	@echo "Building Docker image $(DOCKER_IMAGE)"
	docker build -t $(DOCKER_IMAGE) .

# Docker run target: runs Docker container
docker-run:
	@echo "Running Docker container $(DOCKER_IMAGE)"
	@echo "Open http://localhost:$(PORT) to view the extension"
	docker run -it -p $(PORT):80 -v $(pwd):/app $(DOCKER_IMAGE)