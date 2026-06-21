# JobRec — AI Job Recommendation System

A Django web app that scrapes job postings from RemoteOK and Remotive, then ranks them by cosine similarity against your skills and preferences.

## Setup

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Then visit http://127.0.0.1:8000

## How it works

1. Register and fill in your profile (skills, preferred roles, location).
2. The app fetches jobs from RemoteOK and Remotive APIs.
3. Each job's title + description + tags is vectorized with TF-IDF.
4. Your profile is also converted to a weighted TF-IDF vector (skills 3×, roles 2×).
5. Cosine similarity is computed between your vector and every job vector.
6. Jobs are displayed in descending order of match score (0–100%).

## Adding more scrapers

Add a function to `jobs/scrapers.py` and call it inside `fetch_all_jobs()`.

## Project structure

```
jobrec/          Django project config
jobs/
  models.py      UserProfile, JobPosting
  scrapers.py    RemoteOK, Remotive, sample data fallback
  recommender.py TF-IDF + cosine similarity ranking
  views.py       All views
  forms.py       Register + Profile forms
  urls.py        URL routes
templates/jobs/  HTML templates (Bootstrap 5)
```
