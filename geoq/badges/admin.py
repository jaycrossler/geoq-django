from django.contrib import admin

from .models import Badge,BadgeSettings
from singleton_models.admin import SingletonModelAdmin

class BadgeAdmin(admin.ModelAdmin):
    fields = ('icon',)
    list_display = ('id','level')


admin.site.register(Badge, BadgeAdmin)
admin.site.register(BadgeSettings, SingletonModelAdmin)
