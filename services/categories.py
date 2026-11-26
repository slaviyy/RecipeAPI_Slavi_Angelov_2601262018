
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from db.models import Category
from models.models import CategoryCreate, CategoryUpdate


def get_categories(db: Session):
    statement = select(Category).order_by(Category.id)
    return db.scalars(statement).all()


def get_category(db: Session, category_id: int):
    category = db.get(Category, category_id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    return category


def create_category(db: Session, category_data: CategoryCreate):
    normalized_name = category_data.name.strip()

    statement = select(Category).where(
        func.lower(func.trim(Category.name)) == normalized_name.casefold()
    )

    existing_category = db.scalar(statement)

    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category already exists"
        )

    category = Category(name=normalized_name)

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def update_category(
        db: Session,
        category_id: int,
        category_data: CategoryUpdate
):
    category = get_category(db, category_id)

    normalized_name = category_data.name.strip()

    statement = select(Category).where(
        func.lower(func.trim(Category.name)) == normalized_name.casefold(),
        Category.id != category_id
    )

    existing_category = db.scalar(statement)

    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category already exists"
        )

    category.name = normalized_name

    db.commit()
    db.refresh(category)

    return category


def delete_category(db: Session, category_id: int):
    category = get_category(db, category_id)

    db.delete(category)
    db.commit()
