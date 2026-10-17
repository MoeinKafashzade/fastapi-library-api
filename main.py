from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


app = FastAPI(
    title="FastAPI Library API",
    description="A simple library management API using an in-memory Python dictionary.",
    version="1.0.0",
)


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, description="Book title")
    author: str = Field(..., min_length=1, description="Book author")
    published_year: Optional[int] = Field(default=None, ge=0)
    available: bool = True


class BookUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    author: Optional[str] = Field(default=None, min_length=1)
    published_year: Optional[int] = Field(default=None, ge=0)
    available: Optional[bool] = None


class Book(BookCreate):
    id: int


# Dictionary keys are book IDs, so lookups by ID are O(1) on average.
books: dict[int, Book] = {
    1: Book(
        id=1,
        title="The Little Prince",
        author="Antoine de Saint-Exupéry",
        published_year=1943,
        available=True,
    ),
    2: Book(
        id=2,
        title="Animal Farm",
        author="George Orwell",
        published_year=1945,
        available=True,
    ),
    3: Book(
        id=3,
        title="The Old Man and the Sea",
        author="Ernest Hemingway",
        published_year=1952,
        available=False,
    ),
}

# The next ID is kept in memory too. It is initialized above the largest sample ID.
next_book_id = max(books.keys(), default=0) + 1


@app.get("/", tags=["General"])
def root():
    return {"message": "Welcome to the FastAPI Library API", "docs": "/docs"}


@app.get("/books", response_model=list[Book], tags=["Books"])
def list_books():
    """Return all books."""
    return list(books.values())


@app.post(
    "/books",
    response_model=Book,
    status_code=status.HTTP_201_CREATED,
    tags=["Books"],
)
def create_book(book_data: BookCreate):
    """Create a book and assign it a new ID."""
    global next_book_id

    book = Book(id=next_book_id, **book_data.model_dump())
    books[next_book_id] = book
    next_book_id += 1
    return book


@app.get("/books/{book_id}", response_model=Book, tags=["Books"])
def get_book(book_id: int):
    """Return one book by ID."""
    book = books.get(book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} was not found.",
        )
    return book


@app.patch("/books/{book_id}", response_model=Book, tags=["Books"])
def update_book(book_id: int, book_data: BookUpdate):
    """Update only the fields supplied by the client."""
    book = books.get(book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} was not found.",
        )

    updates = book_data.model_dump(exclude_unset=True)
    updated_book = book.model_copy(update=updates)
    books[book_id] = updated_book
    return updated_book


@app.delete("/books/{book_id}", tags=["Books"])
def delete_book(book_id: int):
    """Delete a book by ID."""
    deleted_book = books.pop(book_id, None)
    if deleted_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} was not found.",
        )

    return {
        "message": "Book deleted successfully.",
        "book": deleted_book,
    }
