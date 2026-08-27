# Running Echomart

## Prerequisites

- Git
- Docker Desktop with Compose enabled
- GNU Make (`make`) for the shortcuts in the root Makefile

On Windows, Git Bash, WSL, or another environment that provides GNU Make can be used. The commands below are run from the project root.

## First-time setup

1. Copy `.env.example` to `.env`.
2. Replace `SECRET_KEY` and `POSTGRES_PASSWORD` with local values.
3. Start the services:

   ```bash
   make up
   ```

The services are then available at:

| Service          | Address                                             |
| ---------------- | --------------------------------------------------- |
| Frontend         | http://localhost:5173                               |
| Backend API      | http://localhost:8000                               |
| Swagger API docs | http://localhost:8000/api/docs/                     |
| Django admin     | http://localhost:8000/admin/                        |
| PostgreSQL       | localhost:5432 (inside the Compose network as `db`) |

The backend applies migrations and collects static files when it starts. The Postgres data, uploaded media, and collected static files are stored in named Docker volumes.

## Useful commands

```bash
make help           # List available shortcuts
make logs           # Follow all service logs
make restart        # Restart containers without rebuilding
make migrate        # Apply pending migrations
make makemigrations # Create migrations after model changes
make shell          # Open a Django shell
make test           # Run backend tests
make lint           # Run frontend ESLint
make down           # Stop and remove containers
make clean          # Stop containers and remove volumes
```

Use `make clean` only when deleting local database and uploaded-media state is intentional.

## Rebuilding and rollback

```bash
make rebuild  # Snapshot current images, rebuild without cache, recreate services
make rollback # Restore the most recent complete image snapshot
```

Rollback restores images only. It does not reverse database migrations. If a migration is incompatible with the previous application version, follow the team's migration recovery decision with the backend owner before changing the database.

## Running without Docker

Docker is the recommended team workflow. For backend-only work, SQLite remains the default when `DB_ENGINE` is not set to `postgres`:

```bash
cd backend
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

In another terminal:

```bash
cd vite-frontend
npm ci
npm run dev
```

The frontend uses `VITE_API_URL` when provided and otherwise targets `http://127.0.0.1:8000/`.
