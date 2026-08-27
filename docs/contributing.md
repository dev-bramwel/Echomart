# Team Contribution Guide

## Repository map

- `backend/accounts`: users, authentication, and profiles
- `backend/products`: categories and product catalog behavior
- `backend/vendors`: vendor records and vendor operations
- `backend/orders`: order behavior
- `backend/payments`: payment behavior and provider integrations
- `backend/config`: Django settings, URL routing, and WSGI/ASGI entry points
- `vite-frontend/src`: active React application
- `deployments`: Dockerfiles and frontend web-server configuration
- `docs`: team development documentation

## Change boundaries

Prefer the smallest change that owns the behavior. Keep API contracts explicit and update the frontend integration when a response shape, URL, authentication rule, or error behavior changes. Avoid drive-by formatting and unrelated refactors in feature branches.

## Backend checklist

- Add tests for new endpoint, serializer, permission, model, and validation behavior.
- Use migrations for every model schema change.
- Check authentication and authorization paths explicitly.
- Do not log passwords, tokens, payment credentials, or personal data.
- Confirm the API remains usable by the current frontend or document the required coordinated change.

## Frontend checklist

- Cover loading, success, empty, error, and authenticated states where applicable.
- Check keyboard access, readable errors, and responsive layouts.
- Keep API calls in the existing API integration area rather than duplicating request configuration.
- Run `make lint` and manually verify the affected flow.

## Environment and data

Use `.env.example` as the list of supported local variables. Keep real values in an untracked `.env`. Never use production credentials locally. Treat `make clean` as destructive because it removes the local Postgres volume and uploaded media.

## Pull request checklist

- [ ] Branch is based on current `main`.
- [ ] Tests and linting pass, or failures are explained.
- [ ] `make format-check` passes.
- [ ] Migrations are included and reviewed when models changed.
- [ ] Documentation and `.env.example` are updated when setup changes.
- [ ] UI changes include screenshots or a recording.
- [ ] No secrets or generated artifacts are included.
- [ ] Development log entry is added.
