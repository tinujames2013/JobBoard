from django import forms
from adminpanel.models import Job, Profile, NotificationPreference, Application,NotificationPreference, Profile, Notification


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'email',  # Added missing field
            'job_title', 'job_location', 'job_region', 'job_type', 
            'job_description', 'qualifications', 'salary', 
            'company_name', 'company_tagline', 'company_description', 
            'company_website', 'featured_image', 'logo', 'status'
        ]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'name', 
            'email', 
            'mobile', 
            'company', 
            'date_of_birth', 
            'about_me', 
            'experience', 
            'skills', 
            'profile_picture'
        ]
class NotificationPreferenceForm(forms.ModelForm):
    class Meta:
        model = NotificationPreference
        fields = ['email_alerts', 'new_job_alerts', 'application_status_updates']


class CandidateSearchForm(forms.Form):
    skills = forms.CharField(required=False, max_length=255, label='Skills')
    location = forms.CharField(required=False, max_length=255, label='Location')
    experience = forms.CharField(required=False, max_length=255, label='Experience')

class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status']

class MessageForm(forms.Form):
    subject = forms.CharField(max_length=255, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)




class NotificationPreferenceForm(forms.ModelForm):
    class Meta:
        model = NotificationPreference
        fields = ['email_alerts', 'new_job_alerts', 'application_status_updates']
        widgets = {
            'email_alerts': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'new_job_alerts': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'application_status_updates': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'mobile', 'company', 'about_me']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'about_me': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class NotificationForm(forms.ModelForm):
    """
    Form for sending notifications to candidates.
    """
    class Meta:
        model = Notification
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your message...',
                'rows': 3,
            }),
        }
        labels = {
            'message': 'Message',
        }


class MessageForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, label="Message to Candidate")




class JobFilterForm(forms.Form):
    status = forms.ChoiceField(choices=Job.STATUS_CHOICES, required=False)
    job_title = forms.CharField(max_length=100, required=False)


