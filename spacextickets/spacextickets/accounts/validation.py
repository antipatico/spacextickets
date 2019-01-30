import re
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def is_valid_name(name):
    return name and (re.match(r"^[a-zA-Z]+( [a-zA-Z]+)*$", name) is not None)


def validate_first_name(self):
    first_name = self.cleaned_data['first_name']
    first_name = first_name.strip()
    if not is_valid_name(first_name):
        raise ValidationError(_("Invalid first name, it can only contains letters and spaces."))
    return first_name


def validate_last_name(self):
    last_name = self.cleaned_data['last_name']
    last_name = last_name.strip()
    if not is_valid_name(last_name):
        raise ValidationError(_("Invalid last name, it can only contains letters and spaces."))
    return last_name


def validate_password(password):
    if not password or len(password) < 8:
        raise ValidationError(_("Password must be at least 8 characters long."))


def validate_passwords(password1, password2):
    if not password1 or not password2 or password1 != password2:
        raise ValidationError(_("Passwords don't match"))
