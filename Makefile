.PHONY: install test docker-build docker-run docker-test clean

IMAGE_NAME := mini-assignment-3

# Install dependencies
install:
	python -m pip install -r requirements.txt

# Run tests from Testing folder
test:
	python -m pytest -vv Testing/

# Build the Docker image
docker-build:
	docker build -t $(IMAGE_NAME) .

# Run the test suite from Testing folder inside Docker
docker-test:
	docker run --rm $(IMAGE_NAME) python -m pytest -vv Testing/

# Clean generated files
clean:
	rm -rf __pycache__
	rm -rf .pytest_cache