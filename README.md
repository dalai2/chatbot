# FastAPI Chat Service

## Overview

This is a FastAPI-based chat service that provides an endpoint for handling user conversations. The service is containerized using Docker and includes testing with `pytest`.

## Features

- REST API for handling chat requests
- Dependency injection with FastAPI
- Containerized deployment with Docker
- Automated testing with `pytest`

## Installation

To set up the project, follow these steps:

### Prerequisites

- Python 3
- Docker & Docker Compose

### Setup

1. Clone the repository:

   ```sh
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```

2. Install dependencies:

   ```sh
   make install
   ```

## Running the Service

To start the service using Docker:

```sh
make run
```

This will build and start the containers.

To stop the service:

```sh
make down
```

To remove all stopped containers:

```sh
make clean
```

## Running Tests

To run the test suite:

```sh
make test
```

This will execute `pytest` inside the Docker container.

## API Endpoints

### `POST /chat`

Handles chat interactions.

#### Request Body

```json
{
  "conversation_id": "",
  "message": "The weather is nice, defend otherwise"
}
```

the conversation_id key is required but can be an empty string to start a new conversation, to continue the conversation the id is required.

#### Response

```json
{
  "conversation_id": "12345",
  "message": "The weather is not nice"
}
```
