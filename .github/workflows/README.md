# GitHub Actions

`pull-request-checks.yml` runs automatically for pull requests whose target branch is `main` or `develop`.

It checks:

- Python formatting with Black
- Django system checks and backend tests
- Frontend ESLint checks and production build
- Docker Compose interpolation and configuration
- Backend, frontend, and database image builds

The workflow does not deploy or push images. Configure branch protection in GitHub to require the `Backend checks`, `Frontend checks`, and `Deployment checks` jobs before merging.
