from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.deprecation import CallableTrue, CallableFalse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin


GENDER_CHOICES = (
    ("M", _("Male")),
    ("F", _("Female")),
)


class BaseUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=20, verbose_name=_('first name'))
    last_name = models.CharField(max_length=20, verbose_name=_('last name'))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name=_('gender'))
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name=_('registration date'))
    is_staff = False
    is_active = False
    is_superuser = False

    def get_full_name(self):
        return (_('Mr.') if self.gender == 'M' else _('Ms.')) + ' ' + self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name

    def is_guest(self):
        return type(self) is GuestUser or GuestUser.objects.filter(pk=self.pk).exists()

    USERNAME_FIELD = 'first_name'  # To fix __str__
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender']

    class Meta:
        verbose_name = _('base user')
        verbose_name_plural = _('base users')


class GuestUser(BaseUser):
    email = models.CharField(max_length=30, verbose_name=_('email address'))

    USERNAME_FIELD = 'email'


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("Email is a mandatory field for user."))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class User(BaseUser):
    email = models.CharField(max_length=30, unique=True, verbose_name=_('email address'))
    is_active = models.BooleanField(default=True, verbose_name=_('active'))
    is_staff = models.BooleanField(default=False, verbose_name=_('is staff'))
    is_superuser = models.BooleanField(default=False, verbose_name=_('is superuser'))

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email if self.is_superuser else super().get_full_name()

    def get_short_name(self):
        return self.email if self.is_superuser else super().get_short_name()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class Traveler(models.Model):
    user = models.ForeignKey(BaseUser, null=True, on_delete=models.SET_NULL, verbose_name=_('user'))
    ssn = models.CharField(max_length=15, verbose_name=_('social security number'))
    first_name = models.CharField(max_length=20, verbose_name=_('first name'))
    last_name = models.CharField(max_length=20, verbose_name=_('last name'))
    email = models.CharField(max_length=30, verbose_name=_('email address'))
    state = models.ForeignKey('core.State', verbose_name=_('nationality'))
    birthday = models.DateField(verbose_name=_('birthday date'))
    phone_num = models.CharField(max_length=10, blank=True, verbose_name=_('phone number'))

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        verbose_name = _('traveler')
        verbose_name_plural = _('travelers')
