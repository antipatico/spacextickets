from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from datetime import timedelta
from django.forms import ValidationError


class SearchForm(forms.Form):
    departure = forms.CharField(max_length=20, label=_('Departure'))
    arrival = forms.CharField(max_length=20, label=_('Arrival'))
    dep_date = forms.DateField(label=_('Departure date'))
    dep_time = forms.TimeField(label='Departure time', required=False)
    ret_date = forms.DateField(label=_('Return date'), required=False)
    ret_time = forms.TimeField(label='Departure time', required=False)
    seats = forms.IntegerField(label=_('Number of seats'))

    def clean(self):
        if self.errors:
            return
        data = self.cleaned_data
        dep_date = data["dep_date"]
        dep_time = data["dep_time"]
        ret_date = data["ret_date"]
        ret_time = data["ret_time"]
        if ret_date:
            if dep_date > ret_date:
                raise ValidationError(_("Return date must be greater or equal than departure date."))
            if dep_date == ret_date and (dep_time or ret_time):
                if dep_time and not ret_time:
                    ret_time = dep_time + timedelta(minutes=1)
                    data["ret_time"] = ret_time
                elif ret_time and not dep_time:
                    dep_time = ret_time - timedelta(minutes=1)
                    data["dep_time"] = dep_time
                elif dep_time >= ret_time:
                    raise ValidationError(_("Return time must be greater than departure time."))

                if ret_date == timezone.now().date() or ret_time < timezone.now().time():
                    raise ValidationError(_("Can't search a trip back in the past."))
        return data

    def clean_dep_date(self):
        date = self.cleaned_data['dep_date']
        if date < timezone.now().date():
            raise ValidationError(_("Can't search a trip back in the past."))
        return date

    def clean_seats(self):
        seats = self.cleaned_data['seats']
        if seats < 1:
            raise ValidationError(_("Number of seats must be more than zero"))
        return seats

    def clean_dep_time(self):
        if 'dep_date' in self.cleaned_data:
            dep_time = self.cleaned_data['dep_time']
            if dep_time:
                dep_date = self.cleaned_data['dep_date']
                if dep_date == timezone.now().date() and dep_time < timezone.now().time():
                    raise ValidationError(_("Can't search a trip back in the past."))
            return dep_time

