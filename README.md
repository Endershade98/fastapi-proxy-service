# FastAPI Proxy Server

## Overview

The FastAPI Proxy Server is an asynchronous API gateway designed to forward, control, and optimize HTTP traffic between clients and upstream services. It is built with a strong focus on clean architecture, testability, and production readiness.

The system provides core gateway capabilities such as request forwarding, caching, rate limiting, and structured logging, while maintaining a modular and extensible design suitable for enterprise backend environments.

---

## Architecture

The project follows Clean Architecture principles with a strict separation of concerns:
```Interfaces → Application → Domain → Infrastructure```

### Layers

- **Interfaces**
  - FastAPI routes and middleware
  - HTTP request/response handling

- **Application**
  - Use cases implementing business logic
  - Orchestration of domain and infrastructure services

- **Domain**
  - Core entities, value objects, and business rules
  - Framework-independent abstractions

- **Infrastructure**
  - External services implementations (Redis, HTTP clients, databases, logging)

This structure ensures high maintainability, testability, and scalability.

---

## Core Features

### Proxy Engine
- Asynchronous HTTP request forwarding using httpx
- Transparent request/response handling
- Pluggable request pipeline

### Caching Layer
- Cache abstraction supporting in-memory and Redis backends
- Cache key generation and TTL management
- Designed for extension to distributed caching systems

### Rate Limiting
- IP-based request throttling
- Configurable policies
- Middleware-based enforcement

### Logging and Observability
- Structured logging system
- MongoDB-compatible logging adapter
- Extensible for centralized observability stacks (ELK, OpenTelemetry)

### Resilience
- Retry handling mechanisms for unstable upstream services
- Safe request execution patterns
- Fault-tolerant design principles

---

## Testing Strategy

The project uses a multi-layer testing approach:

- Unit tests for domain logic and use cases
- Integration tests for infrastructure components
- End-to-end tests for full proxy workflows

Testing stack:
- pytest
- httpx test client
- asyncio-based test execution

Current status:
- All tests passing
- Coverage approximately 73%

---

## Tech Stack

- FastAPI
- Uvicorn
- httpx
- Pydantic v2
- Motor (MongoDB async driver)
- Redis (planned/optional backend)
- Pytest

---

## Project Structure
```
app/
├── application/ # Use cases (business logic)
├── domain/ # Core business rules and entities
├── infrastructure/ # External systems integrations
├── interfaces/ # FastAPI routes and middleware
├── bootstrap/ # Dependency injection container
├── config/ # Configuration management
├── utils/ # Shared utilities
```


---

## Setup

### Requirements
- Python 3.14+
- pip

### Installation

```bash
python3.14 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
### Running Tests
```bash
pytest
```

### Running the Application
```bash
uvicorn app.main:app --reload
```
# Design Goals

This project is designed to demonstrate:

- Backend system design using clean architecture principles
- Asynchronous programming with FastAPI
- Infrastructure abstraction for scalable systems
- Production-oriented testing strategy
- Modular design suitable for enterprise environments

# Status

Active development. The system is currently transitioning from a functional proxy prototype to a production-grade backend gateway service.


---

If you want, I can next help you upgrade this into a **GitHub “portfolio-grade README”** with:

- badges (tests, coverage, python version)
- architecture diagram (clean ASCII or Mermaid)
- “engineering highlights” section tailored for recruiters
- or a CV-ready project description aligned with backend job postings
