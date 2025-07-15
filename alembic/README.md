# 🧬 Database Structure & Migrations

This document explains how the database layer of the project is structured and managed using **SQLAlchemy ORM** and **Alembic**.

---

## 📊 Initialize Database
To set up the database, run the following command:

```bash
    alembic upgrade head
```
This will create the database schema based on the current models defined in the codebase and the .env configuration.

## 🗃️ Database Overview

| Technology | Description                     |
|------------|---------------------------------|
| SQLite     | Lightweight embedded DB         |
| SQLAlchemy | ORM used for defining models    |
| Alembic    | Database versioning & migrations |

> 🔐 In case we want to replace SQLite with PostgreSQL is straightforward — just change the connection string in `.env`.

---

## 📐 Schema Design

Currently, the database contains a single table:

### 📄 `samples` table



| Column Name      | Type        | Description                    |
|------------------|-------------|-------------------------------|
| sample_id        | UUID (str)  | Primary key                   |
| sample_type      | Enum        | blood, saliva, tissue         |
| subject_id       | String      | Participant ID                |
| collection_date  | Date        | Sample collection date        |
| status           | Enum        | collected, processing, archived |
| storage_location | String      | Freezer/shelf location        |


Models are defined using SQLAlchemy's Declarative Base in:  
```python
app/db/models.py
````

---

## 🏗️ Migration Workflow (Alembic)

### 🧰 Autogenerate migration scripts

Whenever you **modify models**, generate a new migration file:

```bash
  alembic revision --autogenerate -m "Migration Message"
```

💡 Alembic will compare the current state of your models (`Base.metadata`) with the current DB schema.

---

### 🚀 Apply migrations

To apply the latest migrations:

```bash
    alembic upgrade head
```

To downgrade (rollback):

```bash
    alembic downgrade -1
```

---

## 🔗 Configuration Flow

```ascii
.env --> configuration.py --> SQLAlchemy engine --> Alembic env.py
```

* Connection string is read from `.env`
* Loaded via `pydantic.BaseSettings` in `configuration.py`
* Passed into SQLAlchemy + injected into Alembic's `env.py`

---

## 🗃️ Example `.env` for SQLite

```env
DATABASE_URL=sqlite:///./test.db
```

For PostgreSQL:

```env
DATABASE_URL=postgresql://user:password@localhost/sampledb
```

---

## 🧪 Local Dev Tips

* Delete `test.db` to reset schema (for SQLite)
* Recreate DB + apply migrations:

```bash
    rm test.db
    alembic upgrade head
```

* Inspect the DB (optional):

```bash
    sqlite3 test.db
```

---

## 📁 Migration Files

All migration scripts live in:

```
alembic/versions/
```

Each file includes an `upgrade()` and `downgrade()` function written in SQLAlchemy's migration DSL.
