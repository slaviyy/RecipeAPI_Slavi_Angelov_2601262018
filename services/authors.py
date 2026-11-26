
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from db.models import Author
from models.models import AuthorCreate, AuthorUpdate


def get_authors(db: Session):
    statement = select(Author).order_by(Author.id)
    return db.scalars(statement).all()


def get_author(db: Session, author_id: int):
    author = db.get(Author, author_id)

    if author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found"
        )

    return author


def create_author(db: Session, author_data: AuthorCreate):
    email = str(author_data.email).strip().lower()

    existing_author = db.scalar(
        select(Author).where(
            func.lower(Author.email) == email
        )
    )

    if existing_author:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An author with this email already exists"
        )

    author = Author(
        name=author_data.name.strip(),
        email=email
    )

    db.add(author)
    db.commit()
    db.refresh(author)

    return author


def update_author(
        db: Session,
        author_id: int,
        author_data: AuthorUpdate
):
    author = get_author(db, author_id)

    update_data = author_data.model_dump(exclude_unset=True)

    if "name" in update_data:
        if update_data["name"] is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Author name cannot be null"
            )

        author.name = update_data["name"].strip()

    if "email" in update_data:
        if update_data["email"] is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Author email cannot be null"
            )

        email = str(update_data["email"]).strip().lower()

        existing_author = db.scalar(
            select(Author).where(
                func.lower(Author.email) == email,
                Author.id != author_id
            )
        )

        if existing_author:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An author with this email already exists"
            )

        author.email = email

    db.commit()
    db.refresh(author)

    return author


def delete_author(db: Session, author_id: int):
    author = get_author(db, author_id)

    if author.recipes:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete an author who has recipes"
        )

    db.delete(author)
    db.commit()

    return {"message": "Author deleted successfully"}
