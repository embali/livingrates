from django import forms
from django.core.exceptions import ValidationError

from .models import Account


class SignUpForm(forms.ModelForm):
    full_name = forms.CharField(max_length=128)
    password_ = forms.CharField(max_length=128, widget=forms.PasswordInput())
    confirmation = forms.CharField(max_length=128,
                                   widget=forms.PasswordInput())

    class Meta:
        model = Account
        fields = ['full_name', 'email', 'password_', 'confirmation', ]

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        names = [name.strip() for name in full_name.strip().split()]
        if not names:
            raise ValidationError('Empty name')
        return full_name


class SignInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=128, widget=forms.PasswordInput())


class ResetForm(forms.Form):
    email = forms.EmailField()


class UpdateForm(forms.ModelForm):
    full_name = forms.CharField(max_length=128)
    password_ = forms.CharField(max_length=128, widget=forms.PasswordInput())
    new = forms.CharField(max_length=128, widget=forms.PasswordInput(),
                          required=False)
    confirmation = forms.CharField(max_length=128,
                                   widget=forms.PasswordInput(),
                                   required=False)

    class Meta:
        model = Account
        fields = ['full_name', 'email', 'password_', 'new', 'confirmation', ]

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        names = [name.strip() for name in full_name.strip().split()]
        if not names:
            raise ValidationError('Empty name')
        return full_name
