from django.db import models
from django.contrib.auth.models import User


class ApplicantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    desired_position = models.CharField(max_length=200, blank=True)
    resume = models.TextField(blank=True)
    portfolio_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def initials(self):
        fn = (self.user.first_name or "").strip()
        ln = (self.user.last_name or "").strip()
        initials = ""
        if fn:
            initials += fn[0].upper()
        if ln:
            initials += ln[0].upper()
        if initials:
            return initials
        return (self.user.username[:2].upper() if self.user.username else "")

    def __str__(self):
        return f"{self.user.username} ({self.user.get_full_name()})"
