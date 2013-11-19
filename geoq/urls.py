from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from core.views import Dashboard

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', Dashboard.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^geoq/', include('core.urls')),
    url(r'^maps/', include('maps.urls')),
    url(r'^accounts/$',
        'django.contrib.auth.views.login',),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login',),
    url(r'^accounts/logout/$',
        'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^badges/', include('badges.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
