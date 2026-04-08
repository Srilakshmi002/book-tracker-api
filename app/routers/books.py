from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import models, schemas, auth
from app.database import get_db

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=schemas.BookResponse, status_code=201)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Add a new book to your reading list."""
    new_book = models.Book(**book.model_dump(), owner_id=current_user.id)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.get("/", response_model=List[schemas.BookResponse])
def get_books(
    status: Optional[str] = Query(None, description="Filter by status: want_to_read, reading, completed"),
    genre: Optional[str] = Query(None, description="Filter by genre"),
    is_favorite: Optional[bool] = Query(None, description="Filter favorites only"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Get all your books with optional filters and pagination."""
    query = db.query(models.Book).filter(models.Book.owner_id == current_user.id)

    if status:
        query = query.filter(models.Book.status == status)
    if genre:
        query = query.filter(models.Book.genre.ilike(f"%{genre}%"))
    if is_favorite is not None:
        query = query.filter(models.Book.is_favorite == is_favorite)

    return query.offset(skip).limit(limit).all()


@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Get reading statistics for the current user."""
    books = db.query(models.Book).filter(models.Book.owner_id == current_user.id).all()

    total = len(books)
    completed = [b for b in books if b.status == "completed"]
    reading = [b for b in books if b.status == "reading"]
    want_to_read = [b for b in books if b.status == "want_to_read"]
    favorites = [b for b in books if b.is_favorite]
    rated = [b.rating for b in books if b.rating is not None]

    return {
        "total_books": total,
        "completed": len(completed),
        "currently_reading": len(reading),
        "want_to_read": len(want_to_read),
        "favorites": len(favorites),
        "average_rating": round(sum(rated) / len(rated), 2) if rated else None,
    }


@router.get("/{book_id}", response_model=schemas.BookResponse)
def get_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Get a single book by its ID."""
    book = db.query(models.Book).filter(
        models.Book.id == book_id,
        models.Book.owner_id == current_user.id
    ).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=schemas.BookResponse)
def update_book(
    book_id: int,
    book_update: schemas.BookUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Update a book's details (title, status, rating, notes, etc.)."""
    book = db.query(models.Book).filter(
        models.Book.id == book_id,
        models.Book.owner_id == current_user.id
    ).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = book_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}", status_code=204)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """Delete a book from your reading list."""
    book = db.query(models.Book).filter(
        models.Book.id == book_id,
        models.Book.owner_id == current_user.id
    ).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()