
from fastapi import FastAPI

from routers.authors import router as authors_router
from routers.categories import router as categories_router
from routers.ingredients import router as ingredients_router
from routers.recipes import router as recipes_router
from routers.recipe_ingredients import router as recipe_ingredients_router

app = FastAPI(
    title="Recipe API",
    description="REST API for managing recipes, authors, categories and ingredients",
    version="1.0.0"
)

app.include_router(authors_router)
app.include_router(categories_router)
app.include_router(ingredients_router)
app.include_router(recipes_router)
app.include_router(recipe_ingredients_router)

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
