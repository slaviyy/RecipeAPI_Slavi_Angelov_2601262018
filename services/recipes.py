from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from db.models import Recipe, Author, Category
from db.models import RecipeIngredient, Ingredient
from models.models import RecipeCreate, RecipeUpdate
from models.models import RecipeScaledResponse


def get_recipes(
        db: Session,
        title: str | None = None,
        category_id: int | None = None,
        max_preparation_time: int | None = None
):
    statement = select(Recipe)

    conditions = []

    if title is not None:
        title = title.strip()

        if title:
            conditions.append(Recipe.title.ilike(f"%{title}%"))

    if category_id is not None:
        conditions.append(Recipe.category_id == category_id)

    if max_preparation_time is not None:
        conditions.append(
            Recipe.preparation_time <= max_preparation_time
        )

    if conditions:
        statement = statement.where(*conditions)

    statement = statement.order_by(Recipe.id)

    return db.scalars(statement).all()


def get_recipe(db: Session, recipe_id: int):
    recipe = db.get(Recipe, recipe_id)

    if recipe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )

    return recipe


def check_author(db: Session, author_id: int):
    author = db.get(Author, author_id)

    if author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found"
        )

    return author


def check_category(db: Session, category_id: int | None):
    if category_id is None:
        return None

    category = db.get(Category, category_id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    return category


def check_unique_title(
        db: Session,
        title: str,
        author_id: int,
        exclude_recipe_id: int | None = None
):
    statement = select(Recipe).where(
        Recipe.author_id == author_id,
        func.lower(func.trim(Recipe.title)) == title.strip().lower()
    )

    if exclude_recipe_id is not None:
        statement = statement.where(
            Recipe.id != exclude_recipe_id
        )

    existing_recipe = db.scalar(statement)

    if existing_recipe:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This author already has a recipe with this title"
        )


def create_recipe(db: Session, recipe_data: RecipeCreate):
    check_author(db, recipe_data.author_id)
    check_category(db, recipe_data.category_id)

    normalized_title = recipe_data.title.strip()

    check_unique_title(
        db,
        normalized_title,
        recipe_data.author_id
    )

    recipe = Recipe(
        title=normalized_title,
        instructions=recipe_data.instructions,
        preparation_time=recipe_data.preparation_time,
        servings=recipe_data.servings,
        author_id=recipe_data.author_id,
        category_id=recipe_data.category_id,
        difficulty=recipe_data.difficulty.value
    )

    try:
        db.add(recipe)
        db.commit()
        db.refresh(recipe)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Recipe conflicts with existing data"
        )

    return recipe


def update_recipe(
        db: Session,
        recipe_id: int,
        recipe_data: RecipeUpdate
):
    recipe = get_recipe(db, recipe_id)

    update_data = recipe_data.model_dump(exclude_unset=True)

    if not update_data:
        return recipe

    # These fields cannot be NULL.
    required_fields = {
        "title",
        "instructions",
        "preparation_time",
        "servings",
        "author_id",
        "difficulty"
    }

    for field in required_fields:
        if field in update_data and update_data[field] is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"{field} cannot be null"
            )

    new_author_id = update_data.get("author_id", recipe.author_id)
    new_category_id = update_data.get("category_id", recipe.category_id)
    new_title = update_data.get("title", recipe.title)

    check_author(db, new_author_id)
    check_category(db, new_category_id)

    check_unique_title(
        db,
        new_title,
        new_author_id,
        exclude_recipe_id=recipe_id
    )

    if "difficulty" in update_data:
        update_data["difficulty"] = update_data["difficulty"].value

    for field, value in update_data.items():
        setattr(recipe, field, value)

    try:
        db.commit()
        db.refresh(recipe)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Recipe conflicts with existing data"
        )

    return recipe


def delete_recipe(db: Session, recipe_id: int):
    recipe = get_recipe(db, recipe_id)

    db.delete(recipe)
    db.commit()


def get_recipes_by_author(db: Session, author_id: int):
    author = db.get(Author, author_id)

    if author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found"
        )

    statement = (
        select(Recipe)
        .where(Recipe.author_id == author_id)
        .order_by(Recipe.id)
    )

    return db.scalars(statement).all()


def get_scaled_recipe(
        db: Session,
        recipe_id: int,
        requested_servings: int
):
    recipe = get_recipe(db, recipe_id)

    statement = (
        select(RecipeIngredient, Ingredient.name)
        .join(
            Ingredient,
            RecipeIngredient.ingredient_id == Ingredient.id
        )
        .where(RecipeIngredient.recipe_id == recipe_id)
        .order_by(Ingredient.id)
    )

    results = db.execute(statement).all()

    ingredients = []

    for recipe_ingredient, ingredient_name in results:
        new_quantity = (
                recipe_ingredient.quantity
                * requested_servings
                / recipe.servings
        )

        ingredients.append({
            "ingredient_id": recipe_ingredient.ingredient_id,
            "ingredient_name": ingredient_name,
            "quantity": new_quantity,
            "unit": recipe_ingredient.unit
        })

    recipe_data = {
        "id": recipe.id,
        "title": recipe.title,
        "instructions": recipe.instructions,
        "preparation_time": recipe.preparation_time,
        "servings": recipe.servings,
        "author_id": recipe.author_id,
        "category_id": recipe.category_id,
        "difficulty": recipe.difficulty,
        "requested_servings": requested_servings,
        "ingredients": ingredients
    }

    return RecipeScaledResponse(**recipe_data)
