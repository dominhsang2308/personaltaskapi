# Task Management API

A modern FastAPI-based Personal Task API using MongoDB and Redis.

## Features
- **Architecture**: Distributed system (FastAPI + MongoDB + Redis).
- **Authentication**: JWT-based auth via FastAPI-Users.
- **Database**: Document-oriented storage with Beanie ODM.
- **Caching**: Performance optimization using Redis.
- **Advanced API**: Pagination, filtering, sorting, and task statistics.

## Setup & Running

### Using Docker (Recommended)
The easiest way to run the entire stack (API, MongoDB, Redis) is using Docker Compose:

1. Clone the repository.
2. Run:
   ```bash
   docker-compose up --build
   ```
3. The API will be available at: `http://localhost:8000`
4. Documentation (Swagger): `http://localhost:8000/docs`

### Local Setup
1. Create a virtual environment: `python -m venv venv`
2. Activate it: `venv\Scripts\activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Set up environment variables in `.env`:
   - `MONGODB_URL`: mongodb://localhost:27017/taskapi
   - `REDIS_URL`: redis://localhost:6379
   - `SECRET_KEY`: your_secret_key
5. Run the app: `python main.py`


