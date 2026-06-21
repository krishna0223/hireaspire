from django.contrib import admin
from .models import UserProfile, JobPosting

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'skills', 'preferred_roles', 'experience_years')

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'source', 'posted_at')
    list_filter = ('source',)
    search_fields = ('title', 'company', 'tags')
