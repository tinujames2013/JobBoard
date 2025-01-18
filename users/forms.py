from django import forms
from adminpanel.models import Profile, Job,Application,NotificationPreference,CandidateDocument
from django.core.exceptions import ValidationError
from adminpanel.models import Job , Application

from adminpanel.validators import validate_file_type



class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume', 'cover_letter']
        widgets = {
            'resume': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.odt,.xls,.xlsx,.ppt,.pptx',
            }),
            'cover_letter': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.odt,.xls,.xlsx,.ppt,.pptx',
            }),
        }
        labels = {
            'resume': 'Upload Resume',
            'cover_letter': 'Upload Cover Letter (Optional)',
        }
        help_texts = {
            'resume': 'Allowed file types: PDF, DOC, DOCX,  ',
            'cover_letter': 'Allowed file types: PDF, DOC, DOCX,  ',
        }






class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'mobile', 'company', 'date_of_birth', 'about_me', 'experience', 'skills','profile_picture']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'skills': forms.TextInput(attrs={'placeholder': 'Comma-separated skills, e.g., Python, Django'}),
        }



class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'mobile', 'date_of_birth', 'about_me', 'experience', 'skills']

class DocumentUploadForm(forms.Form):
    resume = forms.FileField(label="Upload Resume")
    additional_documents = forms.FileField(label="Additional Documents (Optional)", required=False)


class JobSearchForm(forms.Form):
    keyword = forms.CharField(required=False, label="Keyword")
    location = forms.CharField(required=False, label="Location")
    category = forms.ChoiceField(
        choices=[('IT', 'IT'), ('Finance', 'Finance'), ('Healthcare', 'Healthcare')], required=False
    )




class JobSearchForm(forms.Form):
    location = forms.CharField(max_length=100, required=False, label="Location")
    category = forms.CharField(max_length=100, required=False, label="Category")
    min_salary = forms.IntegerField(required=False, label="Minimum Salary")
    max_salary = forms.IntegerField(required=False, label="Maximum Salary")



class NotificationPreferenceForm(forms.ModelForm):
    class Meta:
        model = NotificationPreference
        fields = ['email_alerts', 'new_job_alerts', 'application_status_updates']

class WithdrawApplicationForm(forms.Form):
    confirm_withdrawal = forms.BooleanField(required=True, label="I confirm I want to withdraw my application.")



class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = CandidateDocument
        fields = ['resume', 'portfolio', 'certifications']
        widgets = {
            'resume': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'portfolio': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'certifications': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
