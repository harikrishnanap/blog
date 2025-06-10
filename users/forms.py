from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.utils.safestring import mark_safe
from django.contrib.auth.password_validation import password_validators_help_texts


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Style username help text
        username_help = """
            <ul class='username-help'>
                <li>150 characters or fewer.</li>
                <li>Letters, digits and @/./+/-/_ only.</li>
            </ul>
            """
        self.fields['username'].help_text = mark_safe(username_help)

        # Format password validation help text as styled <ul>
        password_help = "<ul class='password-help'>"
        for text in password_validators_help_texts():
            password_help += f"<li>{text}</li>"
        password_help += "</ul>"

        self.fields['password1'].help_text = mark_safe(password_help)

        # Password confirmation help text (styled)
        password2_help = """
                <div class='password2-help'>
                    Make sure to enter the same password as above for confirmation.
                </div>
                """
        self.fields['password2'].help_text = mark_safe(password2_help)


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
