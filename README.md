# Recipe API

A REST API application for managing recipes, developed using **Python** and **FastAPI**.

## Technologies

- Python 3.12
- FastAPI
- SQLAlchemy 2.0
- SQLite
- Pydantic 2
- Alembic

## Features

- CRUD operations for authors, recipes, categories, and ingredients.
- Managing ingredients associated with recipes.
- Input data validation.
- Business rules and uniqueness constraints.
- Recipe filtering by title, category, and preparation time.
- Scaling ingredient quantities based on the number of servings.
- Database schema management using Alembic migrations.

## Installation

Clone the repository:

```bash
git clone https://github.com/slaviyy/RecipeAPI_Slavi_Angelov_2601262018.git
cd RecipeAPI_Slavi_Angelov_2601262018
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Database Migration

Create the database and apply migrations:

```bash
alembic upgrade head
```

## Run the Application

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8001
```

## API Documentation

Once the application is running, the interactive API documentation is available at:

**http://127.0.0.1:8001/docs**

## Author

Slavi Angelov
