from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db.database import get_db
from models.models import (
    RecipeIngredientCreate,
    RecipeIngredientUpdate,
    RecipeIngredientResponse
)
import services.recipe_ingredients as ingredient_service


router = APIRouter(
    prefix="/recipes/{recipe_id}/ingredients",
    tags=["Recipe Ingredients"]
)


@router.get("/", response_model=list[RecipeIngredientResponse])
def get_recipe_ingredients(
        recipe_id: int,
        db: Session = Depends(get_db)
):
    return ingredient_service.get_recipe_ingredients(db, recipe_id)


@router.post(
    "/",
    response_model=RecipeIngredientResponse,
    status_code=status.HTTP_201_CREATED
)
def add_ingredient_to_recipe(
        recipe_id: int,
        ingredient_data: RecipeIngredientCreate,
        db: Session = Depends(get_db)
):
    return ingredient_service.add_ingredient_to_recipe(
        db, recipe_id, ingredient_data
    )


@router.put(
    "/{ingredient_id}",
    response_model=RecipeIngredientResponse
)
def update_recipe_ingredient(
        recipe_id: int,
        ingredient_id: int,
        ingredient_data: RecipeIngredientUpdate,
        db: Session = Depends(get_db)
):
    return ingredient_service.update_recipe_ingredient(
        db, recipe_id, ingredient_id, ingredient_data
    )


@router.delete(
    "/{ingredient_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def remove_ingredient_from_recipe(
        recipe_id: int,
        ingredient_id: int,
        db: Session = Depends(get_db)
):
    ingredient_service.remove_ingredient_from_recipe(
        db, recipe_id, ingredient_id
    )