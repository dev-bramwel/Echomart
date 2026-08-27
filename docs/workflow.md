# Development Workflow

## 1. Start from a current branch

```bash
git switch main
git pull --ff-only origin main
git switch -c feature/short-description
```

Use `fix/`, `docs/`, or `chore/` when those prefixes describe the work better than `feature/`. Keep one logical change per branch.

## 2. Before coding

- Read the relevant app, serializer, view, component, and nearby tests.
- Check open work and avoid duplicating an existing branch or issue.
- Confirm the API or UI behavior being changed and its acceptance criteria.
- Start the stack with `make up` when the change needs the integrated services.

## 3. During implementation

- Keep backend changes inside the owning Django app where possible.
- Keep reusable frontend behavior in `vite-frontend/src/Components` or the nearest existing feature area.
- Add or update tests with behavior changes.
- Run `make makemigrations` for model changes, inspect the generated migration, and commit it with the model change.
- Never commit `.env`, credentials, tokens, database files, build output, or `node_modules`.
- Record the day's meaningful changes in the [development log](development-log.md).

## 4. Validate before opening a PR

```bash
make migrate
make test
make lint
git diff --check
git status
```

For integration-sensitive changes, also run `make rebuild`, inspect `make logs`, and verify the affected user flow at `http://localhost:5173`.

## 5. Commit and review

Use small, imperative commit messages that explain the change:

```text
Add vendor product filtering
Fix token refresh handling
Document Docker development setup
```

Push the branch and open a pull request against `main`. The PR description should include:

- What changed and why
- How it was tested
- Migration or environment-variable impact
- Screenshots or a short recording for UI changes
- Known limitations and follow-up work

Request review from the owner of the affected area. Resolve review comments with a new commit or a clear reply, then ensure the branch is current before merge.

## Ownership and handoffs

- Backend/API: review Django models, serializers, views, URLs, permissions, and migrations with a backend owner.
- Frontend: review React routes, components, API integration, and responsive behavior with a frontend owner.
- Payments and authentication: require an additional focused review because failures can affect money or account security.
- Deployment: review Compose, Dockerfiles, environment variables, and rollback behavior with the deployment owner.

A handoff should include the current branch, completed work, remaining risks, commands already run, test status, and the next concrete step.
