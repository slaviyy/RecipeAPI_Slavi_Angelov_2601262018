
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from db.database import get_db
from models.models import RecipeCreate, RecipeUpdate, RecipeResponse
import services.recipes as recipe_service
from models.models import RecipeScaledResponse

router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"]
)


@router.post(
    "/",
    response_model=RecipeResponse,
    status_code=status.HTTP_201_CREATED
)
def create_recipe(
        recipe_data: RecipeCreate,
        db: Session = Depends(get_db)
):
    return recipe_service.create_recipe(db, recipe_data)


@router.get("/", response_model=list[RecipeResponse])
def get_recipes(
        title: str | None = None,
        category_id: int | None = Query(default=None, gt=0),
        max_preparation_time: int | None = Query(default=None, gt=0),
        db: Session = Depends(get_db)
):
    return recipe_service.get_recipes(
        db,
        title,
        category_id,
        max_preparation_time
    )


@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe(
        recipe_id: int,
        db: Session = Depends(get_db)
):
    return recipe_service.get_recipe(db, recipe_id)


@router.put("/{recipe_id}", response_model=RecipeResponse)
def update_recipe(
        recipe_id: int,
        recipe_data: RecipeUpdate,
        db: Session = Depends(get_db)
):
    return recipe_service.update_recipe(
        db,
        recipe_id,
        recipe_data
    )


@router.delete(
    "/{recipe_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_recipe(
        recipe_id: int,
        db: Session = Depends(get_db)
):
    recipe_service.delete_recipe(db, recipe_id)


@router.get("/{recipe_id}/scaled", response_model=RecipeScaledResponse)
def get_scaled_recipe(
        recipe_id: int,
        servings: int = Query(..., ge=1, le=68),
        db: Session = Depends(get_db)
):
    return recipe_service.get_scaled_recipe(
        db,
        recipe_id,
        servings
    )