from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, include, url


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'geoq.views.home', name='home'),
    # url(r'^geoq/', include('geoq.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^geoq/', include('core.urls')),
    url(r'^maps/', include('maps.urls')),

    url(r'^accounts/$',
        'django.contrib.auth.views.login',),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login',),
    url(r'^accounts/logout/$',
        'django.contrib.auth.views.logout_then_login', name='logout'),
)
