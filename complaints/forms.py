from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CitizenRegistrationForm(UserCreationForm):
    # Explicitly define the email field as required
    email = forms.EmailField(required=True, help_text="Used for notifications and password recovery.")

    class Meta:
        model = User
        fields = ("username", "email") # This order determines the form layout

    # Security: Ensure no two users use the same email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use. Please use a different one.")
        return email


