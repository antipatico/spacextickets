from django import forms
from spacextickets.core.models import State
from spacextickets.accounts.models import User, Traveler
from spacextickets.accounts.validation import *


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, required=False)

    guest = False

    def __init__(self, data=None, guest=False, *args, **kwargs):
        super().__init__(data=data, *args, **kwargs)
        self.guest = guest

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'gender', 'password1', 'password2')

    clean_first_name = validate_first_name
    clean_last_name = validate_last_name

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if not self.guest:
            validate_password(password1)
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if not self.guest:
            validate_passwords(password1, password2)
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'gender', 'is_active', 'is_staff')

    clean_first_name = validate_first_name
    clean_last_name = validate_last_name


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'gender')


class PasswordChangeForm(forms.Form):
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password_new1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password_new2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, required=True)

    def clean_password_new1(self):
        password_new1 = self.cleaned_data.get('password_new1')
        validate_password(password_new1)
        return password_new1

    def clean_password_new2(self):
        password_new1 = self.cleaned_data.get("password_new1")
        password_new2 = self.cleaned_data.get("password_new2")
        validate_passwords(password_new1, password_new2)
        return password_new1


class TravelerForm(forms.ModelForm):
    state = forms.ModelChoiceField(widget=forms.Select, queryset=State.objects.all())
    traveler_id = forms.CharField(required=False)

    class Meta:
        model = Traveler
        fields = ('ssn', 'first_name', 'last_name', 'email', 'state', 'birthday', 'phone_num', 'traveler_id')
