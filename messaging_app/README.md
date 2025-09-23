# messaging_app CI/CD

Jenkins pipeline at `messaging_app/Jenkinsfile` uses credentialsId `github-creds` for Git checkout and `docker-hub-creds` for Docker Hub.
GitHub Actions workflows:
  - CI: `.github/workflows/ci.yml` runs Django checks, migrations, pytest with coverage, and flake8; starts a MySQL service.
  - Docker deploy: `.github/workflows/dep.yml` and `.github/workflows/dep.yaml` build and push Docker images to Docker Hub using `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets.

## Jenkins Plugins
  - Git plugin
  - Pipeline
  - ShiningPandaPlugin

## Docker
  - Dockerfile uses Python 3.10 and exposes 8000.
  - docker-compose defines `web` and `db` services with a persisted volume.