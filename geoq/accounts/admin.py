import reversion
from django.contrib.gis import admin
from models import UserProfile, Organization


class OrganizationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Organization, OrganizationAdmin)
