from django.db import models
from django.conf import settings

class UserInformation(models.Model):
    custom_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Basic Info
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    preferred_study_country = models.CharField(max_length=100, blank=True)

    # Academic Info
    current_degree = models.CharField(max_length=100, blank=True, null=True)  # e.g., BSc, MSc
    field_of_study = models.CharField(max_length=100, blank=True, null=True)
    gpa = models.DecimalField(max_digits=4, decimal_places=2,blank=True,null=True)
    gre_score = models.PositiveIntegerField(null=True, blank=True)
    ielts_score = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    toefl_score = models.PositiveIntegerField(null=True, blank=True)
    cgpa_scale = models.DecimalField(max_digits=3, decimal_places=1, default=4.0)  # e.g., 4.0 or 5.0 scale

    # Experience
    has_research_experience = models.BooleanField(default=False)
    research_area = models.CharField(max_length=255, blank=True)
    number_of_publications = models.PositiveIntegerField(default=0)
    work_experience_years = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)

    # CV Upload
    cv_file = models.FileField(upload_to='cv_uploads/', blank=True, null=True)

    # Preferences
    interested_degree = models.CharField(max_length=100, blank=True)  # e.g., MSc, PhD
    preferred_university_type = models.CharField(max_length=100, blank=True)  # e.g., research-focused, affordable

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
