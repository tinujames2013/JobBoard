from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from adminpanel.models import CustomUser
from django.contrib.auth import authenticate


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password")
            if not user.is_active:
                raise forms.ValidationError("This account is inactive")
            # Validate the role field if necessary
            if not user.role:
                raise forms.ValidationError("Invalid user role")
        
        return cleaned_data

    def get_user(self):
        """Retrieve the authenticated user."""
        username = self.cleaned_data.get('username')
        return CustomUser.objects.filter(username=username).first()


class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, label="Role")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username/Email")


class CustomPasswordResetForm(PasswordResetForm):
    pass  # Use the default Django functionality


class CustomSetPasswordForm(SetPasswordForm):
    pass  # Use the default Django functionality

