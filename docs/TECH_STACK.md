# TECH_STACK — Milestone 1

## 1. Architecture
Pattern: Modular monolithic web application for Milestone 1.

Flow:
React client → FastAPI REST API → Service layer → SQLAlchemy ORM → PostgreSQL

Future:
The waste prediction service can later become a separate FastAPI microservice. Do not create that microservice now.

## 2. Frontend
- React
- Vite
- TypeScript
- Tailwind CSS
- React Router
- Axios or native fetch (choose one and use it consistently)
- React Hook Form + Zod preferred for forms/validation
- Browser barcode/QR scanning via @zxing/browser preferred

Version rule:
Do NOT use unpinned `latest` versions.
Before installation, inspect the current official documentation/package registry, choose compatible stable versions, and record exact versions in package.json/lockfile.
Current official React documentation lists React 19.2 as the latest major version, and Vite documents the 8.x line; verify exact current patch versions at implementation time.

## 3. Backend
- Python
- FastAPI
- Pydantic
- SQLAlchemy 2.x
- Alembic
- psycopg (PostgreSQL driver)
- Pandas for CSV processing
- pytest + httpx for API tests

FastAPI version rule:
Pin the exact stable version selected during implementation. Do not use a floating range.

## 4. Database
- PostgreSQL local installation
- Do not replace PostgreSQL with SQLite.
- Do not use MongoDB.
- Do not use Supabase/Firebase for Milestone 1.
- Do not use a Dockerized database unless explicitly needed; the existing local PostgreSQL installation is the target.

PostgreSQL deployment:
Local for Milestone 1.
Cloud migration later should require only environment/configuration changes and normal migrations.

## 5. Version Discovery
At project initialization:
- detect `python --version`
- detect `node --version`
- detect `npm --version` (or package manager)
- detect `psql --version`
- record versions in `docs/ENVIRONMENT.md`
- record exact dependency versions in lockfiles

Do not arbitrarily upgrade installed system software.

## 6. Environment Variables
Backend `.env` should support:
DATABASE_URL
APP_ENV
CORS_ORIGINS
EXPIRY_ALERT_DAYS

Do not hardcode credentials.
Commit `.env.example`; do not commit `.env`.

## 7. Development Tools
- Git
- GitHub
- Postman or Bruno for API testing
- VS Code compatible formatting/linting

Recommended:
- Ruff for Python lint/format
- ESLint
- Prettier

## 8. Security Baseline
- Parameterized ORM queries
- Request validation
- CORS restricted to known local frontend origin
- No secrets in source control
- Tenant scoping on every business-owned query
- Safe error messages
- File upload size/type validation
