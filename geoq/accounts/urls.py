
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

from forms import SignupFormExtra

from userena import views as userena_views

from accounts.views import point_to_404


urlpatterns = patterns('',

    # TODO:Accounts -- when you remove accounts, add this back in
    # # Signup
    # url(r'^(?P<username>[\.\w-]+)/signup/complete/$',
    #    userena_views.direct_to_user_template,
    #    {'template_name': 'userena/signup_complete.html',
    #     'extra_context': {'userena_activation_required': userena_settings.USERENA_ACTIVATION_REQUIRED,
    #                       'userena_activation_days': userena_settings.USERENA_ACTIVATION_DAYS}},
    #    name='userena_signup_complete'),

    # Signup, signin and signout
    url(r'^signup/$',
       point_to_404, name='userena_signup'),
    url(r'^signin/$',
        userena_views.signin,
        {'template_name': 'accounts/templates/accounts/signin_form.html'},
        name='userena_signin'),
    url(r'^signout/$',
       userena_views.signout,
       #{'next_page': 'geoq/'},
       name='userena_signout'),


    # Reset password
    url(r'^password/reset/$',
        point_to_404, name='userena_password_reset'),
    url(r'^password/reset/done/$',
        point_to_404, name='userena_password_reset_done'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        point_to_404, name='userena_password_reset_confirm'),
    url(r'^password/reset/confirm/complete/$', point_to_404),

    # Activate
    url(r'^activate/(?P<activation_key>\w+)/$',
        point_to_404, name='userena_activate'),

    # Retry activation
    url(r'^activate/retry/(?P<activation_key>\w+)/$',
        point_to_404, name='userena_activate_retry'),

    # Change email and confirm it
    url(r'^(?P<username>[\.\w-]+)/email/$',
       point_to_404, name='userena_email_change'),
    url(r'^(?P<username>[\.\w-]+)/email/complete/$',
       point_to_404, name='userena_email_change_complete'),
    url(r'^(?P<username>[\.\w-]+)/confirm-email/complete/$',
       point_to_404, name='userena_email_confirm_complete'),
    url(r'^confirm-email/(?P<confirmation_key>\w+)/$',
       point_to_404, name='userena_email_confirm'),

    # Disabled account
    url(r'^(?P<username>[\.\w-]+)/disabled/$',
       point_to_404, name='userena_disabled'),

    # Change password
    url(r'^(?P<username>[\.\w-]+)/password/$',
       point_to_404, name='userena_password_change'),
    url(r'^(?P<username>[\.\w-]+)/password/complete/$',
       point_to_404, name='userena_password_change_complete'),

    # Edit profile
    url(r'^(?P<username>[\.\w-]+)/edit/$',
       point_to_404, name='userena_profile_edit'),

    # View profiles
    url(r'^(?P<username>(?!signout|signup|signin)[\.\w-]+)/$',
       RedirectView.as_view(url='/geoq'),
       name='userena_profile_detail'),
    # url(r'^(?P<username>(?!signout|signup|signin)[\.\w-]+)/$',
    #    point_to_404, name='userena_profile_detail'),
    url(r'^page/(?P<page>[0-9]+)/$',
       point_to_404, name='userena_profile_list_paginated'),
    url(r'^$',
       point_to_404, name='userena_profile_list'),

    # If nothing overrides the urls, then load the default with userena.
    url(r'^', include('userena.urls')),
)