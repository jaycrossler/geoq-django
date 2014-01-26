from django.conf.urls.defaults import *

from .views import overview, detail

urlpatterns = patterns('',
    url(r'^$', overview, name="badges_overview"),
    url(r'^(?P<slug>[A-Za-z0-9_-]+)/$', detail, name="badge_detail"),
    )