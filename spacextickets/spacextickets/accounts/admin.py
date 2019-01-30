from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import register

from .forms import UserCreationForm, UserChangeForm
from .models import *


@register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'get_full_name', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'gender')}),
        (_('Account Info'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'gender', 'password1', 'password2'),
        }),
        (_('Account Info'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')}),
    )

    def get_full_name(self, user):
        return user.get_full_name()

    get_full_name.short_description = _('Full Name')


@register(Traveler)
class TravelerAdmin(admin.ModelAdmin):
    search_fields = ['ssn']
    list_display = ('first_name', 'last_name')
