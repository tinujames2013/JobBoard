from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from adminpanel.models import Profile,Job, Application,NotificationPreference,CandidateDocument,CustomUser
from .forms import ProfileEditForm, ProfileForm, DocumentUploadForm,JobSearchForm, CandidateDocument, ApplicationForm,NotificationPreferenceForm, WithdrawApplicationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.contrib.auth import logout
from django.contrib.auth.models import User  # Import the User model




def home(request):
    """
    Display all published jobs on the home page.
    If the user is not logged in, show a login prompt for applying.
    """
    jobs = Job.objects.all()  # Retrieve all jobs from the database
    return render(request, 'users/users_home.html', {'jobs': jobs})


@login_required
def create_profile(request):
    if hasattr(request.user, 'profile'):
        messages.info(request, "Profile already exists. You can edit it.")
        return redirect('users:edit_profile')

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "Profile created successfully!")
            return redirect('users:view_profile')
    else:
        form = ProfileForm()

    return render(request, 'users/create_profile.html', {'form': form})

@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)  # Handle file uploads
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('users:view_profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'users/edit_profile.html', {'form': form})




@login_required
def edit_candidate_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('users/candidate_profile')
    else:
        form = ProfileEditForm(instance=profile)
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def view_profile(request, username=None):
    if username:
        user = get_object_or_404(CustomUser, username=username)
        profile = get_object_or_404(Profile, user=user)
    else:
        profile = get_object_or_404(Profile, user=request.user)

    # Optionally, you can add more logic here if needed, for example:
    # if request.user != profile.user and not request.user.is_recruiter:
    #     raise PermissionDenied("You are not allowed to view this profile.")
    
    return render(request, 'users/view_profile.html', {'profile': profile})


def my_profile(request):
    if request.user.is_authenticated:
        return redirect('users:view_profile_by_username', username=request.user.username)
    else:
        return redirect('sitevisitor:login')


@login_required
def candidate_dashboard(request):
    profile = get_object_or_404(Profile, user=request.user)
    saved_jobs = request.user.saved_jobs.all()  # Assumes a SavedJob model with a relation to the user.
    applications = request.user.applications.all()  # Assumes an Application model with a relation to the user.
    notifications = request.user.notifications.filter(is_read=False)
    return render(request, 'users/candidate_dashboard.html', {
        'profile': profile,
        'saved_jobs': saved_jobs,
        'applications': applications,
        'notifications': notifications,
    })


@login_required
def upload_documents(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.cleaned_data['resume']
            additional_documents = form.cleaned_data.get('additional_documents')
            # Save documents to the storage
            messages.success(request, "Documents uploaded successfully!")
            return redirect('users/candidate_dashboard')
    else:
        form = DocumentUploadForm()
    return render(request, 'users/upload_documents.html', {'form': form})



def job_list(request):
    search_query = request.GET.get('search', '')
    job_type = request.GET.get('job_type', '')
    job_region = request.GET.get('job_region', '')

    jobs = Job.objects.all()
    if search_query:
        jobs = jobs.filter(job_title__icontains=search_query)
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    if job_region:
        jobs = jobs.filter(job_region=job_region)

    paginator = Paginator(jobs, 6)  # Show 6 jobs per page
    page_number = request.GET.get('page')
    jobs = paginator.get_page(page_number)

    return render(request, 'users/job_list.html', {'jobs': jobs})



def job_detail(request, job_id):
    """
    Display job details and check if the job is saved by the user.
    """
    job = get_object_or_404(Job, id=job_id)
    is_saved = False

    if request.user.is_authenticated:
        is_saved = job.saved_by.filter(id=request.user.id).exists()

    return render(request, 'users/job_detail.html', {
        'job': job,
        'is_saved': is_saved,
    })






def job_expired(request, job_id):
    return render(request, 'users/job_expired.html')

 
def job_search(request):
    form = JobSearchForm()
    return render(request, 'users/job_search.html', {'form': form})

def job_search_results(request):
    form = JobSearchForm(request.GET)
    jobs = Job.objects.all()
    
    if form.is_valid():
        location = form.cleaned_data.get('location')
        category = form.cleaned_data.get('category')
        min_salary = form.cleaned_data.get('min_salary')
        max_salary = form.cleaned_data.get('max_salary')

        if location:
            jobs = jobs.filter(job_location__icontains=location)
        if category:
            jobs = jobs.filter(job_category__icontains=category)
        if min_salary is not None:
            jobs = jobs.filter(salary__gte=min_salary)
        if max_salary is not None:
            jobs = jobs.filter(salary__lte=max_salary)

    return render(request, 'users/job_search_results.html', {'jobs': jobs, 'form': form})




def application_status(request):
    applications = Application.objects.filter(applicant=request.user)
    return render(request, 'users/application_status.html', {'applications': applications})

def withdraw_application(request, application_id):
    application = get_object_or_404(Application, id=application_id, applicant=request.user)
    if request.method == 'POST':
        form = WithdrawApplicationForm(request.POST)
        if form.is_valid():
            application.delete()
            messages.success(request, "Your application has been withdrawn successfully.")
            return redirect('users/application_status')
    else:
        form = WithdrawApplicationForm()
    return render(request, 'users/withdraw_application.html', {'form': form, 'application': application})

def candidate_notifications(request):
    preferences, created = NotificationPreference.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = NotificationPreferenceForm(request.POST, instance=preferences)
        if form.is_valid():
            form.save()
            messages.success(request, "Notification preferences updated successfully.")
            return redirect('users/candidate_notifications')
    else:
        form = NotificationPreferenceForm(instance=preferences)
    return render(request, 'users/candidate_notifications.html', {'form': form})

def candidate_email_preview(request):
    # Example data to simulate an email preview
    email_content = {
        'subject': "Your Application Status Update",
        'body': "Dear Candidate,\n\nYour application status has been updated. Please check your profile for more details.",
    }
    return render(request, 'users/candidate_email_preview.html', {'email_content': email_content})



@login_required
def upload_documents(request):
    try:
        documents = CandidateDocument.objects.get(user=request.user)
    except CandidateDocument.DoesNotExist:
        documents = None

    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES, instance=documents)
        if form.is_valid():
            document_instance = form.save(commit=False)
            document_instance.user = request.user
            document_instance.save()
            messages.success(request, "Documents uploaded successfully.")
            return redirect('users/upload_documents')
    else:
        form = DocumentUploadForm(instance=documents)

    return render(request, 'users/upload_documents.html', {'form': form, 'documents': documents})

@login_required
def view_resume(request):
    try:
        documents = CandidateDocument.objects.get(user=request.user)
    except CandidateDocument.DoesNotExist:
        documents = None

    return render(request, 'users/view_resume.html', {'documents': documents})




def apply_for_job(request, job_id):
    """
    Handles the job application process.
    """
    job = get_object_or_404(Job, id=job_id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user  # Assuming user is authenticated
            application.save()
            messages.success(request, "Your application has been submitted successfully!")
            return redirect('users:job_detail', job_id=job.id)
        else:
            messages.error(request, "There was an error in your application. Please fix the issues and try again.")
    else:
        form = ApplicationForm()

    return render(request, 'users/job_application.html', {
        'form': form,
        'job': job,
    })

def application_list(request):
    """
    View for listing all applications for the logged-in user.
    """
    applications = Application.objects.filter(applicant=request.user)
    return render(request, 'users/application_status.html', {
        'applications': applications,
    })


def view_application(request, id):
    application = get_object_or_404(Application, id=id)
    return render(request, 'users/my_applications.html', {'application': application})

from django.contrib.auth.decorators import login_required

@login_required
def my_applications(request):
    """
    View for candidates to see their applications and statuses.
    """
    applications = request.user.applications.select_related('job')
    return render(request, 'users/my_applications.html', {'applications': applications})


def logout_view(request):
    logout(request)
    return redirect('sitevisitor:home')
