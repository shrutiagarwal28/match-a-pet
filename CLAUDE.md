# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

**Match-A-Pet** is a Django web application connecting pet shelters with adopters. Key workflows:
- Shelters register, add pets, and manage adoption requests
- Users browse/filter pets, save favorites, and request adoption
- Adoption flow: `pending → complete` (shelter confirms → creates owned pet record)
- Direct messaging between users and shelters
- Playdate scheduling between pet owners with owned pets (`ClientUserPet`)
- Mapbox map of shelter locations (geocoded via Google Maps API)

## Commands

```bash
# Install dependencies (Python 3.7)
pip install -r requirements.txt

# Run migrations and start dev server
python manage.py migrate
python manage.py runserver

# Run tests with coverage (as CI does)
coverage run --source=accounts,map manage.py test

# Run a single test module
python manage.py test accounts.tests.test_views

# Lint and format checks
flake8 .
black --check .

# Auto-format
black .
```

## Architecture

### Django Apps

| App | Responsibility |
|-----|---------------|
| `accounts` | Core app: users, shelters, pets, adoption, messaging, favorites |
| `playdate` | Owned pets (`ClientUserPet`) and playdate scheduling |
| `map` | Mapbox map view displaying all shelter locations |

### Data Model Relationships

```
User (AbstractUser + is_shelter / is_clientuser flags)
├── ShelterRegisterData (OneToOne) ← shelter profile & geo coords
├── UserRegisterData (OneToOne)    ← adopter profile & geo coords
└── Message (FK) ← direct messaging system

Pet (shelter-owned, for adoption)
├── shelterRegisterData → ShelterRegisterData
├── favorite (M2M) → User
└── pet_pending_user (M2M) → User

ClientUserPet (user-owned, created on adoption completion or direct registration)
└── userRegisterData → UserRegisterData
```

### Two User Types

The `User.is_shelter` / `User.is_clientuser` boolean flags gate most views and templates. Adoption completion (`adopt_complete` view) auto-creates a `ClientUserPet` record for the adopting user.

### URL Namespacing

All URL patterns are flat (no namespaces). The project `urls.py` includes each app's `urls.py` directly.

### Key Views in `accounts/views.py`

- `register()` — splits into shelter vs. client registration, sends activation email via Gmail SMTP
- `VerificationView` — activates account from email token
- `PetListView` (CBV) — paginated pet list with `django-filter` and `django-tables2`
- `adopt_pending()` / `adopt_complete()` / `adopt_cancel()` — adoption state machine
- `favorite_pet()` — toggles M2M favorite relationship
- `inbox()` / `send_message()` — messaging system with unread count via Django signals

### External APIs

- **Google Maps Geocoding API** — converts user addresses to lat/lng stored on `ShelterRegisterData`/`UserRegisterData`
- **Mapbox** — frontend map rendering in `map/` app

### Testing

Tests live in `accounts/tests/` split across `test_models.py`, `test_views.py`, `test_forms.py`, `test_urls.py`. The `map/` app has `map/tests.py`. Coverage is only tracked for `accounts` and `map` apps.

### CI

Travis CI runs on `develop` (staging) and `main` (production) branches: migrate → collectstatic → black → flake8 → coverage → coveralls.

### Deployment

Heroku via `Procfile` (`gunicorn match_a_pet.wsgi`). `django-heroku` auto-configures `DATABASE_URL` → PostgreSQL in production. Dev uses SQLite (`db.sqlite3`).

### Code Quality Config

Flake8 is configured in `.flake8`: max line length 187, ignores E203/E501/F401/F811. Black is the formatter.
