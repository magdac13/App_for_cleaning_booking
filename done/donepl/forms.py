from django import forms
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.forms import HiddenInput

from donepl.models import User, Customer, Worker, Service, Order


class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'password')
        widgets = {
            'email': forms.TextInput(attrs={'class': 'span2'}),
            'password': forms.PasswordInput(attrs={'class': 'span2'}),
        }


class RegisterForm(forms.ModelForm):
    pass


class ServiceForm(forms.Form):
    name = forms.MultipleChoiceField(
        choices=Service.JOBS_CHOICES,
        required=True,
        widget=forms.CheckboxSelectMultiple
    )

    # def clean_name(self):
    #     for name in self.cleaned_data['name']:
    #         if name not in dict(Service.JOBS_CHOICES):
    #             raise forms.ValidationError('Invalid job')
    #     return self.cleaned_data['name']
#
    # def clean(self):
        # return self.cleaned_data

    class Meta:
        model = Service
        fields = ('name',)


class OrderForm(forms.Form):
    worker_id = forms.IntegerField()
    service = forms.CharField(max_length=200)
    location = forms.CharField(max_length=255)
    hours = forms.IntegerField()

