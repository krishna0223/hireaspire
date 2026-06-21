from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    skills = models.TextField(
        help_text="Comma-separated skills e.g. Python, Django, Machine Learning"
    )
    preferred_roles = models.TextField(
        help_text="Comma-separated job titles e.g. Backend Developer, Data Scientist"
    )
    preferred_locations = models.TextField(
        blank=True,
        help_text="Comma-separated locations e.g. Remote, New York. Leave blank for any."
    )
    experience_years = models.PositiveIntegerField(default=0)

    def skills_list(self):
        return [s.strip() for s in self.skills.split(',') if s.strip()]

    def roles_list(self):
        return [r.strip() for r in self.preferred_roles.split(',') if r.strip()]

    def __str__(self):
        return f"{self.user.username}'s profile"


class JobPosting(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    tags = models.TextField(blank=True, help_text="Comma-separated tags/skills")
    url = models.URLField(max_length=1000)
    source = models.CharField(max_length=100)
    posted_at = models.DateTimeField(auto_now_add=True)
    salary = models.CharField(max_length=100, blank=True)

    def tags_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]

    def searchable_text(self):
        return f"{self.title} {self.company} {self.description} {self.tags} {self.location}"

    class Meta:
        ordering = ['-posted_at']

    def __str__(self):
        return f"{self.title} at {self.company}"
