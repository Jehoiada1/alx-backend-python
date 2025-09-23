# alx-backend-python

## Overview

This repository aggregates Python backend learning exercises (testing, async operations, decorators, generators, etc.) plus a Django REST messaging application (`messaging_app`).

Previously this project contained extensive CI/CD automation (multiple Jenkins pipelines and GitHub Actions workflows). All of those automation files have now been intentionally removed as part of a cleanup/reset request. The application and supporting code remain runnable locally.

## Messaging App: Run Locally

Prerequisites: Python 3.10+ and a local/accessible MySQL instance if you want to mirror production-style settings (or you can point Django to SQLite for quick exploration).

### Quick Start (SQLite for simplicity)
```
cd messaging_app
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
set DJANGO_DEBUG=True
python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000
```

### Running Tests
```
cd messaging_app
python -m pip install pytest pytest-cov
pytest -q
```

### Using MySQL (Optional)
1. Create a database and user.
2. Copy `.env.example` to `.env` and fill in credentials.
3. Install MySQL client build deps (on Linux: `apt-get install default-libmysqlclient-dev build-essential`).
4. Run migrations and start the server.

### Docker (If you still want a container image)
The Docker-related automation was removed, but you can still build manually:
```
cd messaging_app
docker build -t messaging_app:local .
docker run --rm -p 8000:8000 messaging_app:local
```

## Notes
* Optional nested router dependency is handled with a fallback import so the app runs even if `drf-nested-routers` is absent.
* CI/CD artifacts (Jenkinsfiles, GitHub workflow YAMLs) were deleted intentionally; reintroduce them later if automation is needed again.

## Structure Highlights
* `python-generators-0x00/` – Generator pattern exercises
* `python-decorators-0x01/` – Decorator utilities (logging, retry, caching, transactions)
* `python-context-async-perations-0x02/` – Async/context manager examples
* `0x03-Unittests_and_integration_tests/` – Unit & integration test examples
* `messaging_app/` – Django REST messaging service

## Restoring Automation (Future Idea)
If you need CI/CD again, add either a minimal Jenkinsfile at `messaging_app/Jenkinsfile` or a GitHub Actions workflow under `.github/workflows/ci.yml` that installs dependencies and runs `pytest` producing JUnit/coverage reports.

---
Cleanup complete: pipelines and workflows removed as requested.