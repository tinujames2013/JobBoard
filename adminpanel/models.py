from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .validators import validate_file_type

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('candidate', 'Candidate'),
        ('recruiter', 'Recruiter'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='candidate', verbose_name="Role")

    objects = CustomUserManager()

    @property
    def is_candidate(self):
        return self.role == 'candidate'

    @property
    def is_recruiter(self):
        return self.role == 'recruiter'

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100) 
    mobile = models.CharField(max_length=15)
    company = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    about_me = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    skills = models.CharField(max_length=255, blank=True, help_text="Comma-separated skills, e.g., Python, Django, REST API")
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)  # New field
    def __str__(self):
        return self.name


class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('Part Time', 'Part Time'),
        ('Full Time', 'Full Time'),
    ]
    REGION_CHOICES = [
        ('Anywhere', 'Anywhere'),
        ('India', 'India'),
        ('USA', 'USA'),
        ('Canada', 'Canada'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('closed', 'Closed'),
    ]

    email = models.EmailField(help_text="Contact email for this job posting.")
    job_title = models.CharField(max_length=255, db_index=True)
    job_location = models.CharField(max_length=255)
    job_region = models.CharField(max_length=100, choices=REGION_CHOICES, db_index=True)
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES)
    job_description = models.TextField()
    qualifications = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    company_name = models.CharField(max_length=255)
    company_tagline = models.CharField(max_length=255, blank=True, null=True)
    company_description = models.TextField(blank=True, null=True)
    company_website = models.URLField(blank=True, null=True)
    featured_image = models.ImageField(upload_to='job_images/', blank=True, null=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    posted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='jobs')
    posted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')  # New status field

    def __str__(self):
        return self.job_title


class Application(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Reviewed', 'Reviewed'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='resumes/', help_text="Upload your resume.")
    cover_letter = models.FileField(
        upload_to='cover_letters/', 
        null=True, 
        blank=True, 
        help_text="Upload an optional cover letter."
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.username} - {self.job.job_title}"



    
class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"
class SavedJob(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} saved {self.job.job_title}"

class SavedFilter(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='saved_filters')
    name = models.CharField(max_length=50)  # Name for the filter
    filters = models.JSONField()  # Store filter options in JSON format

    def __str__(self):
        return f"{self.user.username}'s filter - {self.name}"

class ActivityLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='activity_logs')
    action = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action} at {self.created_at}"



class NotificationPreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_preference')
    email_alerts = models.BooleanField(default=True, help_text="Receive email alerts for job-related updates.")
    new_job_alerts = models.BooleanField(default=True, help_text="Receive alerts for new job listings.")
    application_status_updates = models.BooleanField(default=True, help_text="Receive application status updates.")



class CandidateDocument(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='documents')
    resume = models.FileField(upload_to='documents/resumes/', blank=True, null=True)
    portfolio = models.FileField(upload_to='documents/portfolios/', blank=True, null=True)
    certifications = models.FileField(upload_to='documents/certifications/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Documents"
