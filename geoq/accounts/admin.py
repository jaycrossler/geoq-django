import reversion
from django.contrib.gis import admin
from models import UserAuthorization, UserProfile, Organization


class ObjectAdmin(reversion.VersionAdmin,):
    pass


class OrganizationAdmin(ObjectAdmin):
    pass

# Unregister userena's admin to add to it.
admin.site.unregister(UserProfile)
class UserProfileAdmin(ObjectAdmin):
    list_display = ('user','organization','score')
    # list_editable = ('organization','authorized',)
    # readonly_fields = ('permissions_granted_by',)

class UserAuthorizationAdmin(ObjectAdmin):
    list_display = ('user_profile','authorized')
    list_editable = ('authorized',)
    readonly_fields = ('permissions_granted_by',)


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserAuthorization, UserAuthorizationAdmin)
