# Buildifo Backend

FastAPI backend foundation for Buildifo.com, using PostgreSQL, SQLAlchemy, and Alembic.

## Run locally

1. Create a PostgreSQL database named `buildifo`.
2. Copy `.env.example` to `.env` and set the database credentials.
3. Install dependencies with `pip install -r requirements.txt`.
4. Apply migrations with `alembic upgrade head`.
5. Start the API with `uvicorn app.main:app --reload`.

The API documentation is available at `/docs`.

## Implemented

- Root and health endpoints
- Customer create, list, read, update, and delete endpoints
- Customer validation, pagination, unique email handling, and timestamps
- CORS configuration
- Initial Alembic migration

## Remaining product work

- Authentication, authorization, user and organization tenancy
- Projects, contractors, estimates, invoices, payments, and file attachments
- Search, activity history, notifications, email, and audit logging
- Production PostgreSQL, secrets, migrations in CI/CD, backups, and monitoring
- Frontend application, deployment configuration, and end-to-end tests