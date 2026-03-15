Task Management API

This is a backend service for managing tasks and projects, built with  FastAPI ,  MongoDB  (Beanie), and  Redis . 

The project focus on high performance and clean architecture, utilizing asynchronous patterns for DB operations and event handling.

     Technical Choices

-  FastAPI : For high-performance, async-first API development.
-  MongoDB + Beanie : Flexible document storage with a strong ODM layer.
-  Redis : Multi-purpose use for caching (performance) and Pub/Sub (event-driven logic).
-  Docker : Simple deployment environment.

Features

-  Auth : JWT-based authentication using `fastapi-users`.
-  Caching : Cache-aside implementation on Task retrieval.
-  Events : Simple Pub/Sub system for task-related events.
-  Aggragation : Real-time stats using MongoDB pipelines.

Setup

Using Docker
The quickest way to get it running:
```bash
docker-compose up --build
```

- API Base: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`

       Local Development
1. Create venv: `python -m venv venv`
2. Activate & Install: `pip install -r requirements.txt`
3. Setup `.env` (copy from template if provided).
4. Run: `python main.py`

     Project Structure

- `src/routes/`: API endpoint definitions.
- `src/crud/`: Core business logic and DB interactions.
- `src/db.py`: Database models and initialization.
- `src/utils/`: Common helpers and utilities.



