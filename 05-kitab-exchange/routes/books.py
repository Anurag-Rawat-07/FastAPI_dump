from fastapi import Depends, HTTPException, APIRouter, Query
from typing import Optional
from sqlmodel import Session, select
from database import get_session

from models.book import Book, BookCreate, BookRead, BookUpdate

from auth import verify_api_key

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=list[BookRead])
def list_books(
    title: Optional[str] = Query(default=None),
    author: Optional[str] = Query(default=None),
    session: Session = Depends(get_session)      #dependency injection for database session
    ):
    query = select(Book).where(                  #writing a query to select books that are not sold
        Book.is_sold == False
    )
    if title:                                              #added filtering for title and author if provided in query parameters
        query = query.where(Book.title.contains(title))    #these are add on to the base query to filter the results based on title and author
    if author:
        query = query.where(Book.author.contains(author))
    
    books = session.exec(query).all()
    return books


@router.post("/", response_model=BookRead)
def create_book(
    book_data: BookCreate,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key)         #for writing information to the database, we need to verify the API key for authentication and authorization
):
    book = Book.model_validate(book_data)          #model validate goes and validate aa the data against the model that you have created
    session.add(book)
    session.commit()         #sql qurries
    session.refresh(book)
    return book


@router.patch("/{book_id}", response_model=BookRead)  #path parameter for book_id, response model is BookRead
def update_book(
    book_id: int,
    updates: BookUpdate,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key)
):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book_data = updates.model_dump(exclude_unset=True)  #converted string to dictionary 
    for key, value in book_data.items():
        setattr(book, key, value)                       #set attribute of the book object to the new value from the updates

    session.add(book)
    session.commit()
    session.refresh(book)
    return book

@router.patch("/{book_id}/sold", response_model=BookRead)
def mark_book_sold(
    book_id: int,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key)
):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book.is_sold = True
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


