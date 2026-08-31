# ENVIRONMENT — Detected Local Versions

Recorded during Phase 0 on 2026-08-31.

## System Tools

| Tool       | Version   | Location                                |
|------------|-----------|-----------------------------------------|
| Python     | 3.13.3    | system PATH                             |
| Node.js    | 22.16.0   | system PATH                             |
| npm        | 11.4.1    | system PATH                             |
| PostgreSQL | 18.6      | `C:\Program Files\PostgreSQL\18\bin\`   |
| psql       | 18.6      | same (not on PATH by default)           |

## PostgreSQL Service

- Service name: `postgresql-x64-18`
- Status: Running
- Target database: `food_rescue`

## Notes

- `psql` is installed but not on the system PATH. All DB interaction uses SQLAlchemy/Alembic.
- Add `C:\Program Files\PostgreSQL\18\bin\` to PATH if direct `psql` access is desired.
- Do not upgrade system-installed tools unless explicitly requested.
