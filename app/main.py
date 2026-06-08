from fastapi import FastAPI

app = FastAPI(title="Travel Planner API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Travel Planner API"}