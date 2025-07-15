# 🧬 Sample Management API

A FastAPI-based backend system to manage biological samples in a research or clinical environment.
It is a Restful API that supports CRUD operations, JWT authentication, test coverage, and Docker support.

---

## 🚀 How to Run the App

### 🔧 Locally (Using Virtual Environment)

1. **Clone the repository**  
```bash
   git clone https://github.com/Sklyvan/SampleManagement.git
   cd SampleManagement/
```

2. **Set Up a Virtual Environment**

```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

3. **Install dependencies**

```bash
   pip install -r requirements.txt
```

4. **Create `.env` file**

```env
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=your_secret_key
HASH_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. **Use Alembic for Database Initialization**

```bash
    alembic upgrade head
```
For more details regarding the Database schema and creation, refer to the [alembic/README.md](alembic/README.md) file.
6. **Run the Application**

```bash
   uvicorn app.main:app --reload --reload-exclude *test*.py
```
The application can be found at [localhost:8000](http://localhost:8000) with the OpenAPI docs available at [localhost:8000/docs](http://localhost:8000/docs).

---

### 🐳 With Docker

We need to initialize the database before running the Docker container. You can do this by running the following command:

```bash
    alembic upgrade head
```

> [!IMPORTANT]  
> The user running the Docker container must have permissions to access the Docker daemon.

Then, you can build and run the Docker container:

```bash
    docker build -t sample-management .
    docker run -p 8000:8000 --env-file .env -v "$(pwd)/test.db:/app/test.db" sample-management
```

---

## ✅ How to Test It

1. **Ensure you're in the root directory and in a virtual environment**
2. Run all tests with:

```bash
   pytest
```

> Tests use an in-memory SQLite database, so no need for `.env` or migrations during testing.

---

## ⚙️ Technologies Used

| Technology      | Why It Was Chosen                                      |
|-----------------|--------------------------------------------------------|
| **FastAPI**     | Fast, typed, modern API development with built-in docs |
| **SQLAlchemy**  | Full-featured ORM with Alembic support                 |
| **Pydantic**    | For strict validation of schemas and config            |
| **Alembic**     | For database migrations                                |
| **Pytest**      | Simple and powerful test runner                        |
| **JWT (OAuth2)** | Secure stateless authentication                        |
| **Docker**      | Easy deployment and reproducibility                    |
| **SQLite**      | Simple way to deal with a basic SQL database           |

---

## ✅ What Was Completed

🔹 Full CRUD endpoints for `Sample` <br>
🔹 Filtering support (`status`, `type`) <br>
🔹 Data validation via Pydantic <br>
🔹 Alembic-based DB migrations <br>
🔹 JWT-based Authentication <br>
🔹 Global route protection with token auth <br>
🔹 Unit tests for all API functionality <br>
🔹 Dockerized build <br>

---

## 🛠️ What Could Be Improved or Added

* Add full user management (registration, password hashing, roles)
* Support pagination on GET endpoints
* Implement more detailed logging and exception tracing
* Add some GitHub Actions CI/CD for automated testing and deployment
* Create a real database of users instead of a hardcoded dictionary
* Use PostgreSQL instead of SQLite for production (or MySQL if preferred)
* Create a Docker Ignore file to exclude unnecessary files
* Use `slowapi` to limit the number of requests

---

## ⚖️ Trade-offs Made

* Kept auth simple (JWT only) to focus on sample domain logic
* Used SQLite and in-memory DB for local/test speed (vs. full Postgres setup)
* No persistent user store (tokens simulate an already-authenticated user)
* Skipped OAuth2 flow in favor of direct token access for brevity

---

## 📁 Project Structure

```
SampleManagement/
├── alembic/                    ← DB migrations
│   ├── versions/               ← Migration scripts
│   ├── env.py                  ← Alembic config
│   ├── README.md               ← Schema docs
├── app/                        ← Main application
│   ├── api/                    ← Routes & auth logic
│   │   ├── authentication.py
│   │   ├── configuration.py
│   │   ├── endpoints.py
│   ├── db/                     ← DB models, session, base
│   │   ├── base.py
│   │   ├── models.py
│   │   ├── session.py
│   ├── schemas/                ← Pydantic schemas
│   │   └── sample.py
│   └── main.py                 ← FastAPI app entrypoint
├── tests/                      ← Unit tests (pytest)
│   ├── conftest.py             ← Test client + test DB
│   └── test_samples.py
├── .env                        ← Secrets (excluded from Git)
├── .gitignore
├── alembic.ini
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 📬 Example API Calls

You can interactively explore and test all endpoints using the built-in OpenAPI docs at [http://localhost:8000/docs](http://localhost:8000/docs).

Below are example `curl` commands for authenticating and using the JWT token with each API endpoint.

### Obtain a JWT Token 🔑

Replace `<username>` and `<password>` with valid credentials.

```bash
    curl -X POST "http://localhost:8000/token" \
         -H "Content-Type: application/x-www-form-urlencoded" \
         -d "username=<username>&password=<password>"
```

The response will include an `access_token` field. Use this token in the `Authorization` header for all subsequent requests:

```bash
    export TOKEN="your_jwt_token_here"
```

### Create a Sample

```bash
    curl -X POST "http://localhost:8000/samples" \
         -H "Authorization: Bearer $TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"sample_id": "S123", "sample_type": "blood", "status": "collected", ...}'
```

### Get a Sample by ID

```bash
    curl -X GET "http://localhost:8000/samples/S123" \
         -H "Authorization: Bearer $TOKEN"
```

### List Samples (with optional filters)

```bash
    curl -X GET "http://localhost:8000/samples?sample_status=collected&sample_type=blood" \
         -H "Authorization: Bearer $TOKEN"
```

### Update a Sample

```bash
    curl -X PUT "http://localhost:8000/samples/S123" \
         -H "Authorization: Bearer $TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"status": "archived"}'
```

### Delete a Sample

```bash
    curl -X DELETE "http://localhost:8000/samples/S123" \
         -H "Authorization: Bearer $TOKEN"
```

> [!TIP]
> You can "play" with all endpoints and see example requests/responses at [localhost:8000/docs](http://localhost:8000/docs).
