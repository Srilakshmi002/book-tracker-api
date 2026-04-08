# Book Tracker API

A Restful backend API built with **FastAPI** and **SQLite** that allows users to manage their personal reading list. 
Features JWT authentication, full CRUD operations, filtering, and reading statistics.

---

## Features
- **JWT Authentication** - Secure register/login with token-based auth
- **Book Management** - Add, update, delete, and view books
- **Reading Status** - Track books as `want_to_read`,`reading`, or `completed`
- **Ratings & Notes** - Rate books (1-5 stars) and add personal notes
- **Favorites** - Mark and filter your favorite books
- **Filter & Pagination** - Filter by status, genre, or favorites with pagination
- **Reading Stats** - See total books, average rating, and reading progress
- **Auto Swagger Docs** - Interactive API docs at `/docs`

---

## Tech Stack
| Tool | Purpose |
| ---- | ------- |
| **FastAPI** | Web framework |
| **SQLite** | Database |
| **Pydantic v2** | Data validation & Serialization |
| **JWT (python-jose)** | Authentication |
| **Passlib + bcrypt** | Password hashing |
| **Uvicorn** | ASGI server |

```
## Project Structure
book-tracker-api/
├── app/
│   ├── auth.py          # JWT logic & password hashing
│   ├── database.py      # SQLAlchemy engine & session
│   ├── models.py        # Database models (User, Book)
│   ├── schemas.py       # Pydantic schemas for validation
│   └── routers/
│       ├── auth.py      # /auth endpoints
│       └── books.py     # /books endpoints
├── main.py              # App entry point
├── requirements.txt
├── .env
└── .gitignore
```

## Getting Started

### 1. Clone the repository
```bash
git clone https"//github.com/yourusername/book-tracker-api.git
cd book-tracker-api
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env .env
```

### 5. Run the server
```bash
uvicorn main:app --reload
```

### 6. Open API docs
Visit **http://127.0.0.1:8000/docs** to explore and test all endpoints.

---

## API Endpoints
### Authentication
| Method | Endpoint | Description |
|-----|----------|-------------|
| POST | `/auth/register` | Create a new account |
| POST | `/auth/login` | Login and receive JWT token |
| GET | `/auth/me` | Get current user info |

### Books (require authentication)
| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| POST | `/books/` | Add a new book |
| GET | `/books/` | Get all books (with filters) |
| GET | `/books/stats` | Get reading statistics |
| GET | `/books/{id}` | Get a specific book |
| PUT | `/books/{id}` | Update a book |
| DELETE | `/books/{id}` | Delete a book |

---

## Future Improvements
- Switch to PostgreSQL
- Add Docker support
- Deploy to Railway or Rendor
- Add search by title/author
