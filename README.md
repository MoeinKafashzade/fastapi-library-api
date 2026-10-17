# FastAPI Library API

A small library-management REST API built with **FastAPI**. It stores books in a Python dictionary in memory, so no database is required.

> **Important:** Data is temporary. Books added or changed while the server is running are lost when the process stops or restarts.

## Features

- List all books
- Add a book
- Get a book by ID
- Partially update a book with `PATCH`
- Delete a book
- Automatic API documentation with Swagger UI
- In-memory dictionary keyed by book ID

## Project structure

```text
fastapi-library-api/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Requirements

- Python 3.10 or newer
- pip

## Install and run

### 1. Create a virtual environment

Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Start the API

```bash
uvicorn main:app --reload
```

The server runs at <http://127.0.0.1:8000>.

Open <http://127.0.0.1:8000/docs> to try every endpoint in Swagger UI.

## API endpoints

| Method | Endpoint | Description | Success response |
|---|---|---|---|
| `GET` | `/books` | List all books | `200 OK` |
| `POST` | `/books` | Add a book | `201 Created` |
| `GET` | `/books/{book_id}` | Get one book | `200 OK` |
| `PATCH` | `/books/{book_id}` | Update supplied fields | `200 OK` |
| `DELETE` | `/books/{book_id}` | Delete a book | `200 OK` |

If a book ID does not exist, the API returns `404 Not Found`.

## Example requests

### List books

```bash
curl http://127.0.0.1:8000/books
```

### Add a book

```bash
curl -X POST http://127.0.0.1:8000/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "published_year": 2008,
    "available": true
  }'
```

The API assigns the ID automatically.

### Get a specific book

```bash
curl http://127.0.0.1:8000/books/1
```

### Partially update a book

Only include the fields you want to change:

```bash
curl -X PATCH http://127.0.0.1:8000/books/1 \
  -H "Content-Type: application/json" \
  -d '{"available": false}'
```

### Delete a book

```bash
curl -X DELETE http://127.0.0.1:8000/books/1
```

## Why use a dictionary?

Books are stored in a dictionary whose keys are IDs:

```python
books = {
    1: Book(...),
    2: Book(...),
}
```

Retrieving an item with `books.get(book_id)`, inserting by key, and deleting by key take **O(1) average time**. This is generally faster than searching through a list, which takes O(n) time in the worst case.

This does **not** mean every request has exactly the same total runtime: response serialization, network transfer, and listing all books still depend on the amount of data. In particular, `GET /books` must process every returned book and is O(n).

## Notes and limitations

- Data is stored in process memory and is not persistent.
- Restarting the server resets the data to the sample books.
- The in-memory dictionary is not shared between multiple worker processes.
- This project is intended for learning and small demonstrations, not as a persistent production library system.

## License

You may use and modify this project for learning or personal projects.
