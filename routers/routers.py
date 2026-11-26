
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db.database import get_db
from models.models import (
    AuthorCreate,
    AuthorUpdate,
    AuthorResponse
)
from services import authors as author_service


router = APIRouter(
    prefix="/authors",
    tags=["Authors"]
)


@router.post(
    "/",
    response_model=AuthorResponse,
    status_code=status.HTTP_201_CREATED
)
def create_author(
        author_data: AuthorCreate,
        db: Session = Depends(get_db)
):
    return author_service.create_author(db, author_data)


@router.get(
    "/",
    response_model=list[AuthorResponse]
)
def get_authors(db: Session = Depends(get_db)):
    return author_service.get_authors(db)


@router.get(
    "/{author_id}",
    response_model=AuthorResponse
)
def get_author(
        author_id: int,
        db: Session = Depends(get_db)
):
    return author_service.get_author(db, author_id)


@router.put(
    "/{author_id}",
    response_model=AuthorResponse
)
def update_author(
        author_id: int,
        author_data: AuthorUpdate,
        db: Session = Depends(get_db)
):
    return author_service.update_author(
        db,
        author_id,
        author_data
    )


@router.delete(
    "/{author_id}"
)
def delete_author(
        author_id: int,
        db: Session = Depends(get_db)
):
    return author_service.delete_author(db, author_id)
