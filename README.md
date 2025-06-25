# Physiobuddy Backend

A lightweight and scalable backend built with FastAPI and PostgreSQL to support user registration, authentication (JWT), and secure user data management for the Physiobuddy Android application.

---

## 🌐 Tech Stack

- FastAPI (Python 3.8+)
- PostgreSQL
- SQLAlchemy
- JWT Authentication
- Pydantic
- Pytest + HTTPX for testing

---

## ⚙️ Prerequisites

Ensure the following are installed:

- Python 3.8+
- PostgreSQL
- Git
- `pip` (Python package installer)
- (Optional) `virtualenv` or `conda` for isolated environments

---

## 🛠 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/physiobuddy_backend.git
cd physiobuddy_backend
```


### 2. Create and activate a virtual environment

#### ✅ Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

#### ✅ Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Set up PostgreSQL database

Ensure PostgreSQL is installed and running. Then create a database named:

```bash
physiobuddy_app
```

You can use:

```sql
CREATE DATABASE physiobuddy_app;
```

Set your DB credentials in `app/database.py` or via environment variables if you’ve configured it that way.

---

### 5. Create database tables

```bash
# In root directory
python -m app.create_tables   
```

---

### 6. Run the server

```bash
uvicorn app.main:app --reload
```

The server will run at `http://127.0.0.1:8000/`

Try visiting:

- `http://127.0.0.1:8000/` – Root endpoint
- `http://127.0.0.1:8000/docs` – Swagger API documentation

---

## ✅ Running Tests

Tests are written using `pytest` and `httpx`.

### Install test dependencies:

```bash
pip install pytest pytest-asyncio httpx
```

### Run all tests:

```bash
pytest
```

✅ Tests include:

- User registration
- User login
- Token response and validation

Test accounts are automatically cleaned up after use.

---

## ✨ Contributing

Pull requests are welcome! For major changes, open an issue first to discuss what you’d like to change.

---

## 📄 License

Apache License 2.0

---

## 💡 Maintainer

Built by [Mehul Dinesh Jain](https://www.linkedin.com/in/mehuldain/) ✨
