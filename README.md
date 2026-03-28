# Match-A-Pet

> This is a personal fork of a team project built for a Software Engineering course taught by Professor Gennadiy Civil during my Master's in Computer Science at New York University. The original project was a collaborative effort; this repo reflects my continued work on it, including a Django 4.2 upgrade and deployment to Render.

A web application that connects pet shelters with potential adopters. Shelters can list available pets, and users can browse, favorite, and request adoption. Also supports direct messaging between users and shelters, playdate scheduling between pet owners, and a map of shelter locations.

## Features

- **Pet adoption** — shelters list pets, users browse and request adoption (pending → complete flow)
- **Swiper** — Tinder-style pet browsing interface
- **Favorites** — save and track pets you're interested in
- **Direct messaging** — between adopters and shelters
- **Playdates** — register your own pet and schedule meetups with other pet owners
- **Shelter map** — Mapbox-powered map showing all registered shelters

## Tech Stack

- **Backend:** Django 4.2, Python 3.9
- **Database:** SQLite (local), PostgreSQL (production)
- **Frontend:** Django Templates, Bootstrap 4
- **Deployment:** Render

## Local Development

**Prerequisites:** Python 3.9+

```bash
# Clone the repo
git clone git@github.com:shrutiagarwal28/match-a-pet.git
cd match-a-pet

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations and start server
python manage.py migrate
python manage.py runserver
```

Visit `http://127.0.0.1:8000`

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | Production | Django secret key |
| `DEBUG` | Optional | Set to `False` in production (default: `True`) |
| `ALLOWED_HOSTS` | Production | Comma-separated list of allowed hostnames |
| `DATABASE_URL` | Production | PostgreSQL connection string (auto-set by Render) |
| `MAPBOX_ACCESS_TOKEN` | Optional | For the shelter map feature |
| `EMAIL_HOST_USER` | Optional | Gmail address for account verification emails |
| `EMAIL_HOST_PASSWORD` | Optional | Gmail app password |

For local dev, none of these are required — SQLite and default settings work out of the box.

## Running Tests

```bash
# Run all tests with coverage
coverage run --source=accounts,map manage.py test

# Run a specific test module
python manage.py test accounts.tests.test_views

# Lint
flake8 .
```

## Deployment

This project is configured for [Render](https://render.com) via `render.yaml`.

To deploy:
1. Fork or connect this repo to your Render account
2. Go to Render Dashboard → **New** → **Blueprint**
3. Select this repository — Render will auto-detect `render.yaml` and provision the web service + PostgreSQL database
4. Add any optional env vars (Mapbox token, email credentials) in the Render dashboard

## Project Structure

```
accounts/       # Core app: users, pets, adoption, messaging, favorites
playdate/       # Owned pets and playdate scheduling
map/            # Mapbox shelter location map
match_a_pet/    # Django project settings and URL config
```
