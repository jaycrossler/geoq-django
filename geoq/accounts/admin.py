import reversion
from django.contrib.gis import admin
from models import UserProfile, Organization


class OrganizationAdmin(admin.ModelAdmin):
    pass

# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user','score')

admin.site.register(Organization, OrganizationAdmin)

# Unregister userena's
# admin.site.unregister(UserProfile)
# # Register our version
# admin.site.register(UserProfile, UserProfileAdmin)

