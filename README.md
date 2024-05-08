# Integrate Challenge

## Overview

This project is set up using FastAPI to create a simple web application. The application is containerized using Docker, ensuring that it can be easily built and run in any environment supporting Docker.

## Requirements

- [Docker](https://www.docker.com/get-started/)
- [Python >= 3.10](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/)

## Local setup

1. Navigate to the project directory.
2. Install the dependencies:
   ```
   poetry install
   ```
3. Run the application:
   ```
   poetry run uvicorn main:app --reload
   ```

## Local setup using Docker

1. Clone the repository.
2. Navigate to the project directory.
3. Build the Docker container:
   ```
   docker build -t integrate-challenge .
   ```
4. Run the Docker container:
   ```
   docker run -p 8000:8000 integrate-challenge
   ```

## Check if the setup is working

Once the application is running, you can access it by navigating to `http://localhost:8000/` in your web browser. This will display a list of examples fetched from the FastAPI application.
