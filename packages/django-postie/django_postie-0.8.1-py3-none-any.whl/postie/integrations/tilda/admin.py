from solo.admin import SingletonModelAdmin
from django.contrib import admin

from .models import Preferences


@admin.register(Preferences)
class PreferencesAdmin(SingletonModelAdmin):
    pass
