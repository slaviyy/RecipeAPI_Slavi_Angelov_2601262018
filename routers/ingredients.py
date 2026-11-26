
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db.database import get_db
from models.models import (
    IngredientCreate,
    IngredientUpdate,
    IngredientResponse
)
import services.ingredients as ingredient_service


router = APIRouter(
    prefix="/ingredients",
    tags=["Ingredients"]
)


@router.post(
    "/",
    response_model=IngredientResponse,
    status_code=status.HTTP_201_CREATED
)
def create_ingredient(
        ingredient_data: IngredientCreate,
        db: Session = Depends(get_db)
):
    return ingredient_service.create_ingredient(db, ingredient_data)


@router.get("/", response_model=list[IngredientResponse])
def get_ingredients(db: Session = Depends(get_db)):
    return ingredient_service.get_ingredients(db)


@router.get("/{ingredient_id}", response_model=IngredientResponse)
def get_ingredient(
        ingredient_id: int,
        db: Session = Depends(get_db)
):
    return ingredient_service.get_ingredient(db, ingredient_id)


@router.put("/{ingredient_id}", response_model=IngredientResponse)
def update_ingredient(
        ingredient_id: int,
        ingredient_data: IngredientUpdate,
        db: Session = Depends(get_db)
):
    return ingredient_service.update_ingredient(
        db, ingredient_id, ingredient_data
    )


@router.delete(
    "/{ingredient_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_ingredient(
        ingredient_id: int,
        db: Session = Depends(get_db)
):
    ingredient_service.delete_ingredient(db, ingredient_id)
