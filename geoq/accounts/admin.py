import reversion
from django.contrib.gis import admin
from models import UserProfile, Organization


class ObjectAdmin(reversion.VersionAdmin,):
    pass


class OrganizationAdmin(ObjectAdmin):
    pass

# Unregister userena's
admin.site.unregister(UserProfile)
class UserProfileAdmin(ObjectAdmin):
    list_display = ('user','score')
    readonly_fields = ('permissions_granted_by',)

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

