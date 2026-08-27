# Formatting, Linting, and Pull Request Checks

## Local commands

Run these commands from the project root while the Docker services are available:

```bash
make format         # Apply Black to Python and ESLint autofixes to frontend code
make format-check   # Check Python formatting and frontend lint rules
make lint           # Run Django checks, Ruff, and frontend ESLint
make test           # Run the Django test suite
make frontend-build # Build the frontend image
```

`make format` changes files. Review the resulting diff before committing. `make format-check` is read-only and is the closest local formatting and lint check to CI.

Backend formatting uses [Black](https://black.readthedocs.io/) and backend linting uses [Ruff](https://docs.astral.sh/ruff/). Frontend formatting currently uses the repository's ESLint configuration with `--fix`; this keeps the check aligned with the existing frontend tooling instead of introducing a second formatter configuration.

## Pull request workflow

The workflow at `.github/workflows/pull-request-checks.yml` runs when a pull request targets either `main` or `develop`. It has three required jobs:

### Backend checks

- Installs `backend/requirements.txt` and Black.
- Checks Python formatting with `black --check .`.
- Checks Python lint rules with `ruff check .`.
- Runs Django's `manage.py check`.
- Runs the backend test suite with `manage.py test`.

### Frontend checks

- Installs the locked npm dependencies with `npm ci`.
- Runs the frontend ESLint check.
- Builds the Vite production bundle.

### Deployment checks

- Loads `.env.example` as the CI environment.
- Validates Compose interpolation with `docker compose config --quiet`.
- Builds the backend, frontend, and database images.

The workflow does not start containers, deploy services, publish images, or run migrations against a shared database. It verifies that the images can be built and that the checked-in Compose configuration is valid.

## Repository protection

Repository maintainers should configure branch protection for `main` and `develop` and require these status checks:

- `Backend checks`
- `Frontend checks`
- `Deployment checks`

Require a pull request and at least one relevant code owner review before merging. Keep branch protection names synchronized with the workflow job names if the workflow is renamed.

## Before opening a PR

```bash
make format-check
make lint
make test
docker compose --env-file .env.example config --quiet
git diff --check
```

For Dockerfile or Compose changes, also run `make build` when Docker image pulls are available. The CI deployment job performs the same image-build coverage on GitHub-hosted runners.
