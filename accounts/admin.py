from django.contrib import admin
from .models import ApplicantProfile


@admin.register(ApplicantProfile)
class ApplicantProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'country', 'desired_position', 'experience_years')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone')
