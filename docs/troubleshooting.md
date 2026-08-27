# Troubleshooting

## Compose refuses to start because a variable is missing

Copy `.env.example` to `.env` and set at least `SECRET_KEY` and `POSTGRES_PASSWORD`. Compose loads `.env` automatically from the project root.

## Backend cannot connect to Postgres

Check service health and logs:

```bash
docker compose ps
make logs
```

The backend uses `db` as the database hostname inside Compose. Do not use `localhost` for the database host from inside the backend container.

## Migrations fail

Inspect the migration and model changes together. Run:

```bash
make logs
make makemigrations
make migrate
```

Do not delete the Postgres volume to bypass a migration failure unless local data can be discarded. Rollback restores application images but does not undo migrations.

## Frontend shows API or CORS errors

Confirm the backend is reachable at `http://localhost:8000` and that `CORS_ALLOWED_ORIGINS` includes `http://localhost:5173`. If the API address changed, update `VITE_API_URL` and rebuild the frontend with `make frontend-build` or `make rebuild`.

## Port already in use

Stop the conflicting process or change the host-side port in `docker-compose.yml`. Keep the container ports unchanged unless the service configuration is changed as well.

## Frontend image build is slow or fails while pulling images

Confirm Docker Desktop is running and that the machine can reach Docker Hub. Retry `docker compose build frontend`. Existing layers may allow a later attempt to complete without downloading everything again.

## Windows command issues

Run Make commands from Git Bash, WSL, or another shell with GNU Make. Docker commands can also be run directly with `docker compose`. PowerShell users can use the equivalent commands from the root Compose file.
