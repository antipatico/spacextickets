from django.contrib.admin import register, ModelAdmin
from django.utils.translation import ugettext_lazy as _
from modeltranslation.admin import TranslationAdmin
from .models import *


@register(State)
class StateAdmin(TranslationAdmin):
    search_fields = ['name']
    list_display = ('name', 'continent', 'get_city_count')

    def get_queryset(self, request):
        qs = super(StateAdmin, self).get_queryset(request)
        qs = qs.annotate(cities_count=models.Count('city'))
        return qs

    def get_city_count(self, obj):
        return obj.cities_count

    get_city_count.short_description = _('number of cities')
    get_city_count.admin_order_field = 'cities_count'


@register(City)
class CityAdmin(TranslationAdmin):
    search_fields = ['name']
    list_display = ('name', 'get_state', 'get_continent')

    def get_state(self, obj):
        return obj.state.name

    def get_continent(self, obj):
        return obj.state.get_continent_display()

    get_state.short_description = _('state')
    get_continent.short_description = _('continent')
    get_state.admin_order_field = 'state'


@register(ScheduledTrip)
class ScheduledTripAdmin(ModelAdmin):
    search_fields = ['departure', 'arrival']
    list_display = ('departure', 'arrival', 'week_day', 'time', 'duration')



