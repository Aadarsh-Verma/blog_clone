from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from authy.models import Profile


def UniqueUser(value):
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError('User with this name already exists')


def UniqueEmail(value):
    if User.objects.filter(email__iexact=value):
        raise ValidationError('Email already exists')


class SignUpForm(forms.ModelForm):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput(), )
    email = forms.CharField(widget=forms.EmailInput())
    bio = forms.CharField(max_length=100)
    picture = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['username', 'password', 'confirm_password', 'email', 'bio', 'picture']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators.append(UniqueUser)

    def clean(self):
        data = super().clean()
        if data.get("password") != data.get("confirm_password"):
            raise ValidationError('Passwords do not match')


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=50)
    email = forms.CharField(widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    bio = forms.CharField(max_length=100)
    picture = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['bio', 'picture', ]
