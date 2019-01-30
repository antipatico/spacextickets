from modeltranslation.translator import register, TranslationOptions
from .models import *


@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(State)
class StateTranslationOptions(TranslationOptions):
    fields = ('name',)
