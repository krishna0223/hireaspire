# HireAspire 🎯

> Job recommendations ranked by *how well they actually match you* — not just keyword stuffing.

HireAspire is a Django web app that aggregates job postings from multiple sources (RemoteOK, Remotive, Arbeitnow, and Indian tech companies via Greenhouse/Lever), then ranks them against your personal skill profile using **TF-IDF vectorization and cosine similarity** — the same family of techniques used in real-world recommendation engines.

No black-box ML, no API keys required out of the box, no nonsense. Just clean, explainable scoring you can read in about 40 lines of Python.

---

## ✨ Features

- 🔍 **Multi-source aggregation** — pulls live listings from RemoteOK, Remotive, Arbeitnow (EU), and curated Indian companies on Greenhouse & Lever
- 🧠 **Cosine similarity ranking** — your skills, preferred roles, and location are weighted and vectorized, then matched against every job posting
- 📊 **Transparent match scores** — every job shows a 0–100% match score, not a mystery ranking
- 👤 **Per-user profiles** — skills, preferred roles, location, and experience all factor into your personal ranking
- 🔄 **On-demand refresh** — pull fresh listings anytime without restarting the server
- 🎨 **Clean Bootstrap 5 UI** — no frontend build step, works out of the box

---

## 🏗️ How it works

```
┌─────────────┐     ┌──────────────┐     ┌────────────────┐     ┌─────────────┐
│  Scrapers   │ ──▶ │  JobPosting  │ ──▶ │  TF-IDF Vector  │ ──▶ │  Cosine Sim │
│ (4 sources) │     │   (SQLite)   │     │   (skills 3x,   │     │  + Ranking  │
└─────────────┘     └──────────────┘     │   roles 2x)     │     └─────────────┘
                                          └────────────────┘
```

1. **Scrape** — `jobs/scrapers.py` pulls listings from public APIs (RemoteOK, Remotive, Arbeitnow) and company-specific Greenhouse/Lever boards
2. **Store** — listings are deduplicated by URL and saved as `JobPosting` records
3. **Vectorize** — your profile (skills weighted 3×, roles 2×, location 1×) and every job description are converted into TF-IDF vectors using `scikit-learn`
4. **Rank** — cosine similarity is computed between your profile vector and each job vector, then sorted descending
5. **Display** — jobs render with a visual match score bar, source badge, and direct apply link

---

## 🚀 Quick start

```bash
git clone <your-repo-url>
cd hireaspire

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Visit **http://127.0.0.1:8000**, register an account, fill in your profile, and hit refresh on the recommendations page.

---

## 📂 Project structure

```
hireaspire/
├── jobrec/                  # Django project settings & root URLs
├── jobs/
│   ├── models.py            # UserProfile, JobPosting
│   ├── scrapers.py          # RemoteOK, Remotive, Arbeitnow, Greenhouse/Lever (India)
│   ├── recommender.py       # TF-IDF + cosine similarity ranking engine
│   ├── views.py             # Auth, profile setup, recommendations, job detail
│   ├── forms.py             # Register + profile forms
│   ├── urls.py               # URL routing
│   └── admin.py             # Django admin registration
├── templates/jobs/          # Bootstrap 5 templates
├── requirements.txt
└── manage.py
```

---

## 🧩 Adding a new job source

Scrapers are intentionally decoupled — adding a new source takes two steps:

```python
# jobs/scrapers.py

def scrape_my_new_source():
    jobs = []
    # ... fetch + normalize into the standard dict shape:
    # {"title", "company", "location", "description", "tags", "url", "source", "salary"}
    return jobs
```

Then register it inside `fetch_all_jobs()`:

```python
def fetch_all_jobs():
    all_jobs = []
    all_jobs.extend(scrape_remoteok())
    all_jobs.extend(scrape_my_new_source())  # 👈 add here
    ...
    return all_jobs
```

That's it — deduplication, ranking, and display all happen automatically.

---

## 🛠️ Tech stack

| Layer | Technology |
|---|---|
| Backend | Django 4+ |
| Recommendation engine | scikit-learn (TF-IDF, cosine similarity) |
| Scraping | requests, BeautifulSoup |
| Database | SQLite (default, swappable) |
| Frontend | Bootstrap 5, vanilla templates |

---

## 🗺️ Roadmap

- [ ] Resume upload → auto-extract skills
- [ ] Email digest of new high-match jobs
- [ ] Save/bookmark jobs
- [ ] Filter by salary range and experience level
- [ ] Swap TF-IDF for sentence-transformer embeddings (semantic matching)

---

## 📄 License

MIT — do whatever you want with it.

---

<p align="center">Built with Django, scikit-learn, and a healthy disregard for black-box recommendation systems.</p># HireAspire 🎯

> Job recommendations ranked by *how well they actually match you* — not just keyword stuffing.

HireAspire is a Django web app that aggregates job postings from multiple sources (RemoteOK, Remotive, Arbeitnow, and Indian tech companies via Greenhouse/Lever), then ranks them against your personal skill profile using **TF-IDF vectorization and cosine similarity** — the same family of techniques used in real-world recommendation engines.

No black-box ML, no API keys required out of the box, no nonsense. Just clean, explainable scoring you can read in about 40 lines of Python.

---

## ✨ Features

- 🔍 **Multi-source aggregation** — pulls live listings from RemoteOK, Remotive, Arbeitnow (EU), and curated Indian companies on Greenhouse & Lever
- 🧠 **Cosine similarity ranking** — your skills, preferred roles, and location are weighted and vectorized, then matched against every job posting
- 📊 **Transparent match scores** — every job shows a 0–100% match score, not a mystery ranking
- 👤 **Per-user profiles** — skills, preferred roles, location, and experience all factor into your personal ranking
- 🔄 **On-demand refresh** — pull fresh listings anytime without restarting the server
- 🎨 **Clean Bootstrap 5 UI** — no frontend build step, works out of the box

---

## 🏗️ How it works

```
┌─────────────┐     ┌──────────────┐     ┌────────────────┐     ┌─────────────┐
│  Scrapers   │ ──▶ │  JobPosting  │ ──▶ │  TF-IDF Vector  │ ──▶ │  Cosine Sim │
│ (4 sources) │     │   (SQLite)   │     │   (skills 3x,   │     │  + Ranking  │
└─────────────┘     └──────────────┘     │   roles 2x)     │     └─────────────┘
                                          └────────────────┘
```

1. **Scrape** — `jobs/scrapers.py` pulls listings from public APIs (RemoteOK, Remotive, Arbeitnow) and company-specific Greenhouse/Lever boards
2. **Store** — listings are deduplicated by URL and saved as `JobPosting` records
3. **Vectorize** — your profile (skills weighted 3×, roles 2×, location 1×) and every job description are converted into TF-IDF vectors using `scikit-learn`
4. **Rank** — cosine similarity is computed between your profile vector and each job vector, then sorted descending
5. **Display** — jobs render with a visual match score bar, source badge, and direct apply link

---

## 🚀 Quick start

```bash
git clone <your-repo-url>
cd hireaspire

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Visit **http://127.0.0.1:8000**, register an account, fill in your profile, and hit refresh on the recommendations page.

---

## 📂 Project structure

```
hireaspire/
├── jobrec/                  # Django project settings & root URLs
├── jobs/
│   ├── models.py            # UserProfile, JobPosting
│   ├── scrapers.py          # RemoteOK, Remotive, Arbeitnow, Greenhouse/Lever (India)
│   ├── recommender.py       # TF-IDF + cosine similarity ranking engine
│   ├── views.py             # Auth, profile setup, recommendations, job detail
│   ├── forms.py             # Register + profile forms
│   ├── urls.py               # URL routing
│   └── admin.py             # Django admin registration
├── templates/jobs/          # Bootstrap 5 templates
├── requirements.txt
└── manage.py
```

---

## 🧩 Adding a new job source

Scrapers are intentionally decoupled — adding a new source takes two steps:

```python
# jobs/scrapers.py

def scrape_my_new_source():
    jobs = []
    # ... fetch + normalize into the standard dict shape:
    # {"title", "company", "location", "description", "tags", "url", "source", "salary"}
    return jobs
```

Then register it inside `fetch_all_jobs()`:

```python
def fetch_all_jobs():
    all_jobs = []
    all_jobs.extend(scrape_remoteok())
    all_jobs.extend(scrape_my_new_source())  # 👈 add here
    ...
    return all_jobs
```

That's it — deduplication, ranking, and display all happen automatically.

---

## 🛠️ Tech stack

| Layer | Technology |
|---|---|
| Backend | Django 4+ |
| Recommendation engine | scikit-learn (TF-IDF, cosine similarity) |
| Scraping | requests, BeautifulSoup |
| Database | SQLite (default, swappable) |
| Frontend | Bootstrap 5, vanilla templates |

---

## 🗺️ Roadmap

- [ ] Resume upload → auto-extract skills
- [ ] Email digest of new high-match jobs
- [ ] Save/bookmark jobs
- [ ] Filter by salary range and experience level
- [ ] Swap TF-IDF for sentence-transformer embeddings (semantic matching)

---

## 📄 License

MIT — do whatever you want with it.

---

<p align="center">Built with Django, scikit-learn, and a healthy disregard for black-box recommendation systems.</p>
