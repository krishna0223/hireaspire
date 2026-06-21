"""
Scrapers for job postings.
- RemoteOK: public JSON API
- Remotive: public JSON API
- Indeed-style fallback: synthetic sample data for demo
"""
import requests
import logging

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; JobRecBot/1.0)"
}


def scrape_remoteok():
    """Fetch jobs from RemoteOK public API."""
    jobs = []
    try:
        resp = requests.get(
            "https://remoteok.com/api",
            headers={**HEADERS, "Accept": "application/json"},
            timeout=10,
        )
        data = resp.json()
        # First element is a notice dict, skip it
        for item in data[1:]:
            if not isinstance(item, dict):
                continue
            jobs.append({
                "title": item.get("position", ""),
                "company": item.get("company", ""),
                "location": "Remote",
                "description": item.get("description", ""),
                "tags": ", ".join(item.get("tags", [])),
                "url": item.get("url", ""),
                "source": "RemoteOK",
                "salary": item.get("salary", ""),
            })
    except Exception as e:
        logger.warning(f"RemoteOK scrape failed: {e}")
    return jobs


def scrape_remotive():
    """Fetch jobs from Remotive public API."""
    jobs = []
    try:
        resp = requests.get(
            "https://remotive.com/api/remote-jobs?limit=50",
            headers=HEADERS,
            timeout=10,
        )
        data = resp.json()
        for item in data.get("jobs", []):
            jobs.append({
                "title": item.get("title", ""),
                "company": item.get("company_name", ""),
                "location": item.get("candidate_required_location", "Remote"),
                "description": item.get("description", ""),
                "tags": ", ".join(item.get("tags", [])),
                "url": item.get("url", ""),
                "source": "Remotive",
                "salary": item.get("salary", ""),
            })
    except Exception as e:
        logger.warning(f"Remotive scrape failed: {e}")
    return jobs


def get_sample_jobs():
    """Fallback sample jobs for demo/testing."""
    return [
        {
            "title": "Senior Python Developer",
            "company": "TechCorp",
            "location": "Remote",
            "description": "We need a senior Python developer with Django and REST API experience. Knowledge of PostgreSQL and Docker is a plus.",
            "tags": "Python, Django, REST API, PostgreSQL, Docker",
            "url": "https://example.com/job/1",
            "source": "Sample",
            "salary": "$120k-$150k",
        },
        {
            "title": "Data Scientist",
            "company": "DataLabs",
            "location": "New York, NY",
            "description": "Looking for a data scientist proficient in Python, pandas, scikit-learn, and machine learning techniques.",
            "tags": "Python, Machine Learning, pandas, scikit-learn, SQL",
            "url": "https://example.com/job/2",
            "source": "Sample",
            "salary": "$110k-$140k",
        },
        {
            "title": "Frontend React Developer",
            "company": "WebWorks",
            "location": "Remote",
            "description": "React developer needed for building modern UIs. Experience with TypeScript, Redux and REST APIs required.",
            "tags": "React, TypeScript, Redux, JavaScript, CSS",
            "url": "https://example.com/job/3",
            "source": "Sample",
            "salary": "$90k-$120k",
        },
        {
            "title": "DevOps Engineer",
            "company": "CloudBase",
            "location": "San Francisco, CA",
            "description": "Seeking DevOps engineer with Kubernetes, Docker, CI/CD pipelines and AWS cloud infrastructure experience.",
            "tags": "Kubernetes, Docker, AWS, CI/CD, Terraform, Linux",
            "url": "https://example.com/job/4",
            "source": "Sample",
            "salary": "$130k-$160k",
        },
        {
            "title": "Machine Learning Engineer",
            "company": "AIVentures",
            "location": "Remote",
            "description": "Build and deploy ML models at scale. Must know Python, TensorFlow or PyTorch, and MLOps practices.",
            "tags": "Python, TensorFlow, PyTorch, MLOps, Machine Learning, Docker",
            "url": "https://example.com/job/5",
            "source": "Sample",
            "salary": "$140k-$180k",
        },
        {
            "title": "Backend Node.js Developer",
            "company": "StartupXYZ",
            "location": "Austin, TX",
            "description": "Node.js developer for our SaaS platform. Experience with Express, MongoDB, and microservices architecture needed.",
            "tags": "Node.js, Express, MongoDB, Microservices, JavaScript",
            "url": "https://example.com/job/6",
            "source": "Sample",
            "salary": "$95k-$125k",
        },
        {
            "title": "Full Stack Django Developer",
            "company": "GrowthCo",
            "location": "Remote",
            "description": "Full stack developer needed. Strong Django backend skills required with React or Vue frontend experience.",
            "tags": "Python, Django, React, PostgreSQL, REST API, Full Stack",
            "url": "https://example.com/job/7",
            "source": "Sample",
            "salary": "$100k-$130k",
        },
        {
            "title": "Data Analyst",
            "company": "AnalyticsPro",
            "location": "Chicago, IL",
            "description": "Analyze business data using SQL, Python and Tableau. Create dashboards and reports for stakeholders.",
            "tags": "SQL, Python, Tableau, Data Analysis, Excel, pandas",
            "url": "https://example.com/job/8",
            "source": "Sample",
            "salary": "$75k-$95k",
        },
    ]

def scrape_arbeitnow():
    """Fetch jobs from Arbeitnow public API (includes many remote + global listings)."""
    jobs = []
    try:
        resp = requests.get(
            "https://www.arbeitnow.com/api/job-board-api",
            headers=HEADERS,
            timeout=10,
        )
        data = resp.json()
        for item in data.get("data", []):
            jobs.append({
                "title": item.get("title", ""),
                "company": item.get("company_name", ""),
                "location": item.get("location", "Remote") or "Remote",
                "description": item.get("description", ""),
                "tags": ", ".join(item.get("tags", [])),
                "url": item.get("url", ""),
                "source": "Arbeitnow",
                "salary": "",
            })
    except Exception as e:
        logger.warning(f"Arbeitnow scrape failed: {e}")
    return jobs

def scrape_remotive_india():
    """Fetch remote jobs from Remotive open to India-based candidates."""
    jobs = []
    try:
        resp = requests.get(
            "https://remotive.com/api/remote-jobs",
            headers=HEADERS,
            timeout=10,
        )
        data = resp.json()
        for item in data.get("jobs", []):
            location = (item.get("candidate_required_location") or "").lower()
            if "india" in location or "worldwide" in location or "anywhere" in location:
                jobs.append({
                    "title": item.get("title", ""),
                    "company": item.get("company_name", ""),
                    "location": item.get("candidate_required_location", "Remote"),
                    "description": item.get("description", ""),
                    "tags": ", ".join(item.get("tags", [])),
                    "url": item.get("url", ""),
                    "source": "Remotive-India",
                    "salary": item.get("salary", ""),
                })
    except Exception as e:
        logger.warning(f"Remotive India scrape failed: {e}")
    return jobs

INDIAN_COMPANIES_GREENHOUSE = [
    "razorpay", "cred", "meesho", "groww", "zerodha", "freshworks",
    "postman", "browserstack", "chargebee", "innovaccer",
]

INDIAN_COMPANIES_LEVER = [
    "swiggy", "urbancompany", "cure-fit", "dunzo", "khatabook",
]


def scrape_greenhouse_india():
    """Fetch jobs from Indian companies using Greenhouse's public job board API."""
    jobs = []
    for company in INDIAN_COMPANIES_GREENHOUSE:
        try:
            resp = requests.get(
                f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs",
                headers=HEADERS,
                timeout=8,
            )
            if resp.status_code != 200:
                continue
            data = resp.json()
            for item in data.get("jobs", []):
                location = item.get("location", {}).get("name", "")
                jobs.append({
                    "title": item.get("title", ""),
                    "company": company.capitalize(),
                    "location": location,
                    "description": item.get("content", ""),
                    "tags": "",
                    "url": item.get("absolute_url", ""),
                    "source": "Greenhouse-India",
                    "salary": "",
                })
        except Exception as e:
            logger.warning(f"Greenhouse scrape failed for {company}: {e}")
    return jobs

def scrape_lever_india():
    """Fetch jobs from Indian companies using Lever's public job board API."""
    jobs = []
    for company in INDIAN_COMPANIES_LEVER:
        try:
            resp = requests.get(
                f"https://api.lever.co/v0/postings/{company}?mode=json",
                headers=HEADERS,
                timeout=8,
            )
            if resp.status_code != 200:
                continue
            data = resp.json()
            for item in data:
                location = item.get("categories", {}).get("location", "")
                jobs.append({
                    "title": item.get("text", ""),
                    "company": company.capitalize(),
                    "location": location,
                    "description": item.get("descriptionPlain", ""),
                    "tags": ", ".join(item.get("tags", [])),
                    "url": item.get("hostedUrl", ""),
                    "source": "Lever-India",
                    "salary": "",
                })
        except Exception as e:
            logger.warning(f"Lever scrape failed for {company}: {e}")
    return jobs

def fetch_all_jobs():
    """Fetch jobs from all sources, return unified list."""
    all_jobs = []
    all_jobs.extend(scrape_remoteok())
    all_jobs.extend(scrape_remotive())
    all_jobs.extend(scrape_remotive_india())
    all_jobs.extend(scrape_arbeitnow())
    all_jobs.extend(scrape_greenhouse_india())
    all_jobs.extend(scrape_lever_india())
    if not all_jobs:
        # Use sample data if scrapers fail (e.g. network restrictions)
        all_jobs.extend(get_sample_jobs())
    return all_jobs