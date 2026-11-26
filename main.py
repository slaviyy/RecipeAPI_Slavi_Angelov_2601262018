
from fastapi import FastAPI


app = FastAPI(
    title="Recipe API",
    description="REST API for managing recipes, authors, categories and ingredients",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to Recipe API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
