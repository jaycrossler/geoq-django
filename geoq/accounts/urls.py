
from django.conf.urls import patterns, include, url
from forms import SignupFormExtra


urlpatterns = patterns('userena.views',

	url(r'^signup/$', 'signup',
		{
		'signup_form': SignupFormExtra,
		'template_name':'accounts/signup.html',
		},),

	url(r'^signin/$', 'signin',
		{
		'template_name':'accounts/signin.html',
		},),

	url(r'^signout/$', 'signout',
		{
		'template_name':'accounts/signout.html',
		},),

    # If nothing overrides the urls, then load the default with userena.
    url(r'^', include('userena.urls')),

)