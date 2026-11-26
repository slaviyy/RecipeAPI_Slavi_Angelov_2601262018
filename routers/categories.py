
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db.database import get_db
from models.models import CategoryCreate, CategoryUpdate, CategoryResponse
import services.categories as category_service


router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
        category_data: CategoryCreate,
        db: Session = Depends(get_db)
):
    return category_service.create_category(db, category_data)


@router.get("/", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return category_service.get_categories(db)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
        category_id: int,
        db: Session = Depends(get_db)
):
    return category_service.get_category(db, category_id)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
        category_id: int,
        category_data: CategoryUpdate,
        db: Session = Depends(get_db)
):
    return category_service.update_category(
        db, category_id, category_data
    )


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
        category_id: int,
        db: Session = Depends(get_db)
):
    category_service.delete_category(db, category_id)
