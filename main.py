from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app import models
from app.routers import auth, books

# Create all database tables
models.Base.metadata.create_all(bind=engine)

# App Setup
app = FastAPI(
    title="📚 Book Tracker API",
    description="""
A RESTful API for tracking your personal reading list.

## Features
- **User Auth** — Register & login with JWT tokens
- **Book Management** — Full CRUD for your book collection
- **Reading Status** — Track books as *Want to Read*, *Reading*, or *Completed*
- **Ratings & Notes** — Rate books (1–5) and add personal notes
- **Favorites** — Mark your favorite books
- **Filters** — Search by status, genre, or favorites
- **Stats** — Get your reading statistics at a glance
    """,
    version="1.0.0",
    contact={
        "name": "Book Tracker API",
        "url": "https://github.com/Srilakshmi002/book-tracker-api",
    },
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(books.router)


# Root
@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Welcome to the Book Tracker API!",
        "docs": "/docs",
        "version": "1.0.0",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}