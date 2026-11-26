
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from db.models import Ingredient, RecipeIngredient
from models.models import IngredientCreate, IngredientUpdate


def get_ingredients(db: Session):
    statement = select(Ingredient).order_by(Ingredient.id)
    return db.scalars(statement).all()


def get_ingredient(db: Session, ingredient_id: int):
    ingredient = db.get(Ingredient, ingredient_id)

    if ingredient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingredient not found"
        )

    return ingredient


def create_ingredient(db: Session, ingredient_data: IngredientCreate):
    normalized_name = ingredient_data.name.strip()

    statement = select(Ingredient).where(
        func.lower(func.trim(Ingredient.name)) == normalized_name.lower()
    )

    existing_ingredient = db.scalar(statement)

    if existing_ingredient:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ingredient already exists"
        )

    ingredient = Ingredient(name=normalized_name)

    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)

    return ingredient


def update_ingredient(
        db: Session,
        ingredient_id: int,
        ingredient_data: IngredientUpdate
):
    ingredient = get_ingredient(db, ingredient_id)

    normalized_name = ingredient_data.name.strip()

    statement = select(Ingredient).where(
        func.lower(func.trim(Ingredient.name)) == normalized_name.lower(),
        Ingredient.id != ingredient_id
    )

    existing_ingredient = db.scalar(statement)

    if existing_ingredient:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ingredient already exists"
        )

    ingredient.name = normalized_name

    db.commit()
    db.refresh(ingredient)

    return ingredient


def delete_ingredient(db: Session, ingredient_id: int):
    ingredient = get_ingredient(db, ingredient_id)

    statement = select(RecipeIngredient).where(
        RecipeIngredient.ingredient_id == ingredient_id
    )

    existing_relation = db.scalar(statement)

    if existing_relation:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete ingredient used in a recipe"
        )

    db.delete(ingredient)
    db.commit()
