from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from .models import UserProfile, JobPosting
from .forms import RegisterForm, UserProfileForm
from .scrapers import fetch_all_jobs, get_sample_jobs
from .recommender import rank_jobs


def home(request):
    return render(request, 'jobs/home.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('recommendations')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created! Set up your profile to get recommendations.')
            return redirect('profile_setup')
    else:
        form = RegisterForm()
    return render(request, 'jobs/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('recommendations')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('recommendations')
    else:
        form = AuthenticationForm()
    return render(request, 'jobs/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile_setup(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            p = form.save(commit=False)
            p.user = request.user
            p.save()
            messages.success(request, 'Profile saved!')
            return redirect('recommendations')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'jobs/profile.html', {'form': form})


@login_required
def recommendations(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        messages.info(request, 'Please set up your profile first.')
        return redirect('profile_setup')

    # Refresh jobs from scrapers if requested or DB is empty
    refresh = request.GET.get('refresh', False)
    if refresh or JobPosting.objects.count() == 0:
        raw_jobs = fetch_all_jobs()
        # Avoid duplicates by URL
        existing_urls = set(JobPosting.objects.values_list('url', flat=True))
        new_jobs = []
        for j in raw_jobs:
            if j['url'] and j['url'] not in existing_urls:
                new_jobs.append(JobPosting(
                    title=j['title'],
                    company=j['company'],
                    location=j['location'],
                    description=j['description'],
                    tags=j['tags'],
                    url=j['url'],
                    source=j['source'],
                    salary=j.get('salary', ''),
                ))
                existing_urls.add(j['url'])
        if new_jobs:
            JobPosting.objects.bulk_create(new_jobs)

    all_jobs = list(JobPosting.objects.all())
    ranked = rank_jobs(profile, all_jobs)

    # Annotate score as percentage
    ranked_display = [
        {'job': job, 'score': round(score * 100, 1)}
        for job, score in ranked
    ]

    return render(request, 'jobs/recommendations.html', {
        'ranked_jobs': ranked_display,
        'profile': profile,
        'total': len(ranked_display),
    })


@login_required
def job_detail(request, pk):
    try:
        job = JobPosting.objects.get(pk=pk)
    except JobPosting.DoesNotExist:
        messages.error(request, 'Job not found.')
        return redirect('recommendations')
    return render(request, 'jobs/job_detail.html', {'job': job})
