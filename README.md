# Travel Planner API

A CRUD RESTful API built with FastAPI and SQLite, demonstrating external API integration (Art Institute of Chicago), data validation, and automated interactive documentation.

## Features Completed
- [x] Full CRUD operations for Projects and Places.
- [x] External API validation (Places are verified against the Art Institute of Chicago API).
- [x] Business logic validations (Max 10 places per project, prevent duplicates, deletion rules).
- [x] **Bonus:** Caching responses from the third-party API (`async_lru`).
- [x] **Bonus:** Pagination for listing endpoints.
- [x] **Bonus:** Dockerized application.
- [x] **Bonus:** Interactive Postman-like documentation via Swagger UI.

*Note: For the simplicity of this technical assessment, all endpoints are kept in `main.py`. For a larger-scale production application, I would use `APIRouter` to modularize the endpoints.*

## How to Run the Application

### Using Docker (Recommended)
1. Clone the repository: `git clone https://github.com/SviatoslavKashyrin/travel-planner.git`
2. Navigate to the project directory: `cd travel-planner`
3. Build and start the container: `docker-compose up --build`
4. The API will be available at `http://localhost:8000`

### Local Setup (Without Docker)
1. Create a virtual environment: `python -m venv venv`
2. Activate it and install dependencies: `pip install -r requirements.txt`
3. Run the server: `uvicorn app.main:app --reload`

## API Documentation (Postman Alternative)
FastAPI automatically generates interactive OpenAPI documentation. You don't need a separate Postman collection to test the endpoints.
Once the server is running, navigate to:
**[http://localhost:8000/docs](http://localhost:8000/docs)**
