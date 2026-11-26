from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from db.models import Recipe, Ingredient, RecipeIngredient
from models.models import RecipeIngredientCreate, RecipeIngredientUpdate


def check_recipe(db: Session, recipe_id: int):
    recipe = db.get(Recipe, recipe_id)

    if recipe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )

    return recipe


def get_recipe_ingredients(db: Session, recipe_id: int):
    check_recipe(db, recipe_id)

    statement = (
        select(RecipeIngredient, Ingredient.name)
        .join(Ingredient, RecipeIngredient.ingredient_id == Ingredient.id)
        .where(RecipeIngredient.recipe_id == recipe_id)
        .order_by(Ingredient.id)
    )

    results = db.execute(statement).all()

    return [
        {
            "ingredient_id": recipe_ingredient.ingredient_id,
            "ingredient_name": ingredient_name,
            "quantity": recipe_ingredient.quantity,
            "unit": recipe_ingredient.unit
        }
        for recipe_ingredient, ingredient_name in results
    ]


def add_ingredient_to_recipe(
        db: Session,
        recipe_id: int,
        ingredient_data: RecipeIngredientCreate
):
    check_recipe(db, recipe_id)

    ingredient = db.get(Ingredient, ingredient_data.ingredient_id)

    if ingredient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingredient not found"
        )

    existing_link = db.get(
        RecipeIngredient,
        (recipe_id, ingredient_data.ingredient_id)
    )

    if existing_link is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ingredient already exists in this recipe"
        )

    recipe_ingredient = RecipeIngredient(
        recipe_id=recipe_id,
        ingredient_id=ingredient_data.ingredient_id,
        quantity=ingredient_data.quantity,
        unit=ingredient_data.unit.value
    )

    db.add(recipe_ingredient)
    db.commit()
    db.refresh(recipe_ingredient)

    return {
        "ingredient_id": ingredient.id,
        "ingredient_name": ingredient.name,
        "quantity": recipe_ingredient.quantity,
        "unit": recipe_ingredient.unit
    }


def update_recipe_ingredient(
        db: Session,
        recipe_id: int,
        ingredient_id: int,
        ingredient_data: RecipeIngredientUpdate
):
    check_recipe(db, recipe_id)

    recipe_ingredient = db.get(
        RecipeIngredient,
        (recipe_id, ingredient_id)
    )

    if recipe_ingredient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingredient not found in this recipe"
        )

    update_data = ingredient_data.model_dump(exclude_unset=True)

    if not update_data:
        return {
            "ingredient_id": ingredient_id,
            "ingredient_name": recipe_ingredient.ingredient.name,
            "quantity": recipe_ingredient.quantity,
            "unit": recipe_ingredient.unit
        }

    for field, value in update_data.items():
        if value is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"{field} cannot be null"
            )

        if field == "unit":
            value = value.value

        setattr(recipe_ingredient, field, value)

    db.commit()
    db.refresh(recipe_ingredient)

    return {
        "ingredient_id": ingredient_id,
        "ingredient_name": recipe_ingredient.ingredient.name,
        "quantity": recipe_ingredient.quantity,
        "unit": recipe_ingredient.unit
    }


def remove_ingredient_from_recipe(
        db: Session,
        recipe_id: int,
        ingredient_id: int
):
    check_recipe(db, recipe_id)

    recipe_ingredient = db.get(
        RecipeIngredient,
        (recipe_id, ingredient_id)
    )

    if recipe_ingredient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingredient not found in this recipe"
        )

    db.delete(recipe_ingredient)
    db.commit()