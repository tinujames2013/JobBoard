from django.shortcuts import render, redirect, get_object_or_404
from adminpanel.models import Job, Application, Profile, CustomUser, NotificationPreference, Notification
from .forms import (JobForm, ProfileForm, NotificationPreferenceForm, CandidateSearchForm, NotificationForm, 
                    ApplicationStatusForm, MessageForm, JobFilterForm)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponseForbidden



@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request, "Job posted successfully!")
            return redirect('jobs:manage_jobs')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = JobForm()
    
    return render(request, 'jobs/post_job.html', {'form': form})


def job_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    return render(request, 'jobs/job_view.html', {'job': job})


@login_required
def manage_jobs(request):
    jobs = Job.objects.filter(posted_by=request.user)
    return render(request, 'jobs/manage_jobs.html', {'jobs': jobs})

@login_required
def create_profile(request):
    try:
        # Attempt to fetch an existing profile for the logged-in user
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        # Create a form with POST data and potentially an existing profile instance
        if profile:
            form = ProfileForm(request.POST, request.FILES, instance=profile)
        else:
            form = ProfileForm(request.POST, request.FILES)

        if form.is_valid():
            # Save the profile to the database
            new_profile = form.save(commit=False)
            new_profile.user = request.user  # Link the profile to the logged-in user
            new_profile.save()
            return redirect('jobs:view_profile')  # Redirect to the view profile page

    else:
        # Create a blank form or pre-fill it if the profile exists
        if profile:
            form = ProfileForm(instance=profile)
        else:
            form = ProfileForm()

    return render(request, 'jobs/create_profile.html', {'form': form, 'profile': profile})

@login_required
def view_profile(request):
    try:
        # Fetch the profile of the logged-in user
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        # Redirect to create_profile if the profile does not exist
        return redirect('jobs:create_profile')

    return render(request, 'jobs/view_profile.html', {'profile': profile})



def home(request):
    posted_jobs = Job.objects.filter(status='active').order_by('-posted_at')[:6]
    return render(request, 'jobs/jobs_home.html', {'posted_jobs': posted_jobs})

@login_required
def recruiter_dashboard(request):
    jobs = Job.objects.filter(posted_by=request.user)
    applications = Application.objects.filter(job__in=jobs)
    notifications = Notification.objects.filter(user=request.user)[:5]

    context = {
        "job_count": jobs.count(),
        "active_job_count": jobs.filter(status="active").count(),
        "expired_job_count": jobs.filter(status="expired").count(),
        "application_count": applications.count(),
        "pending_application_count": applications.filter(status="pending").count(),
        "reviewed_application_count": applications.filter(status="reviewed").count(),
        "notifications": notifications,
    }
    return render(request, "jobs/recruiter_dashboard.html", context)


@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, posted_by=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated successfully!")
            return redirect('jobs:manage_jobs')
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/edit_job.html', {'form': form, 'job': job})

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, posted_by=request.user)
    if request.method == 'POST':
        job.delete()
        messages.success(request, "Job deleted successfully!")
        return redirect('jobs:manage_jobs')
    return render(request, 'jobs/confirm_delete.html', {'job': job})

@login_required
def change_job_status(request, job_id):
    job = get_object_or_404(Job, id=job_id, posted_by=request.user)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        job.status = new_status
        job.save()
        messages.success(request, f"Job status updated to {job.get_status_display()}")
        return redirect('jobs:manage_jobs')
    return render(request, 'jobs/change_status.html', {'job': job})

@login_required
def applications_dashboard(request):
    applications = Application.objects.filter(job__posted_by=request.user)
    return render(request, 'jobs/applications_dashboard.html', {'applications': applications})

@login_required
def application_details(request, application_id):
    application = get_object_or_404(Application, id=application_id, job__posted_by=request.user)
    if request.method == "POST":
        form = ApplicationStatusForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, "Application status updated.")
            return redirect('jobs:applications_dashboard')
    else:
        form = ApplicationStatusForm(instance=application)
    return render(request, 'jobs/application_details.html', {'application': application, 'form': form})

@login_required
def filter_applications(request):
    applications = Application.objects.filter(job__posted_by=request.user)
    status = request.GET.get('status')
    if status:
        applications = applications.filter(status=status)
    return render(request, 'jobs/filter_applications.html', {'applications': applications})

@login_required
def candidate_communication(request, application_id):
    application = get_object_or_404(Application, id=application_id, job__posted_by=request.user)

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            Notification.objects.create(
                user=application.applicant,
                message=message,
            )
            messages.success(request, "Message sent successfully.")
            return redirect('jobs:candidate_communication', application_id=application.id)
    else:
        form = MessageForm()

    return render(request, 'jobs/candidate_communication.html', {
        'form': form,
        'application': application,
    })

@login_required
def update_application_status(request, application_id):
    application = get_object_or_404(Application, id=application_id, job__posted_by=request.user)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Application.STATUS_CHOICES):
            application.status = new_status
            application.save()

            Notification.objects.create(
                user=application.applicant,
                message=f"Your application for '{application.job.job_title}' has been {new_status.lower()}.",
            )
            messages.success(request, "Application status updated successfully!")
        else:
            messages.error(request, "Invalid status selected.")
        return redirect('jobs:applications_dashboard')

    return render(request, 'jobs/application_status_update.html', {
        'application': application,
        'statuses': dict(Application.STATUS_CHOICES),
    })

@login_required
def my_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'users/notifications.html', {
        'notifications': notifications,
    })

def logout_view(request):
    logout(request)
    return redirect('sitevisitor:home')
@login_required
def candidate_search(request):
    form = CandidateSearchForm(request.GET or None)
    results = None
    if form.is_valid():
        skills = form.cleaned_data.get('skills')
        location = form.cleaned_data.get('location')
        experience = form.cleaned_data.get('experience')

        # Query the Profile model
        query = Profile.objects.all()
        if skills:
            query = query.filter(skills__icontains=skills)
        if location:
            query = query.filter(user__profile__location__icontains=location)
        if experience:
            query = query.filter(experience__icontains=experience)

        results = query

    return render(request, 'jobs/candidate_search.html', {'form': form, 'results': results})

@login_required
def recruiter_notifications(request):
    preferences = request.user.notification_preference
    if request.method == "POST":
        preferences.email_alerts = request.POST.get("email_alerts") == "on"
        preferences.new_job_alerts = request.POST.get("new_job_alerts") == "on"
        preferences.application_status_updates = request.POST.get("application_status_updates") == "on"
        preferences.save()
    return render(request, "jobs/recruiter_notifications.html", {"preferences": preferences})

@login_required
def recruiter_profile(request):
    profile = request.user.profile
    if request.method == "POST":
        profile.company = request.POST.get("company_name")
        profile.name = request.POST.get("contact_name")
        profile.email = request.POST.get("email")
        profile.mobile = request.POST.get("mobile")
        profile.about_me = request.POST.get("about_me")
        profile.skills = request.POST.get("skills")
        branding = request.FILES.get("branding")
        if branding:
            profile.branding_logo = branding  # Assuming you have a field branding_logo in the model
        profile.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("jobs:recruiter_profile")
    return render(request, "jobs/recruiter_profile.html", {"profile": profile})



@login_required
def edit_recruiter_profile(request):
    user = request.user
    if request.method == "POST":
        form = RecruiterProfileForm(request.POST, request.FILES, instance=user) # type: ignore
        if form.is_valid():
            form.save()
            return redirect('recruiter_dashboard')
    else:
        form = RecruiterProfileForm(instance=user) # type: ignore
    return render(request, 'edit_recruiter_profile.html', {'form': form, 'user': user})

@login_required
def profile_view(request):
    """View the profile based on the user's role."""
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return redirect('jobs:create_profile')

    if request.user.is_candidate:
        return render(request, 'jobs/candidate_profile.html', {'profile': profile})
    elif request.user.is_recruiter:
        return render(request, 'jobs/recruiter_profile.html', {'profile': profile})


def applications_list(request):
    """
    View to display all applications for recruiters.
    """
    applications = Application.objects.select_related('job', 'applicant').all()
    return render(request, 'jobs/applications_list.html', {'applications': applications})