import reversion
from django.contrib.gis import admin
from models import Project, Job, AOI


class ObjectAdmin(admin.OSMGeoAdmin, reversion.VersionAdmin):
    list_display = ('name', 'created_at', 'updated_at')


class AOIAdmin(ObjectAdmin):
	filter_horizontal = ("reviewers",)
	save_on_top = True

class JobAdmin(ObjectAdmin):
 	filter_horizontal = ("analysts","reviewers","feature_types")
 	save_on_top = True

admin.site.register(Project, ObjectAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(AOI, AOIAdmin)
