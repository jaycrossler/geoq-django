
from django.conf.urls import patterns, include, url
from forms import SignupFormExtra


urlpatterns = patterns('userena.views',

	#Sign up
	url(r'^signup/$', 'signup',
		{'signup_form': SignupFormExtra,
		'template_name':'accounts/signup.html',},),

    # If nothing overrides the urls, then load the default with userena.
    url(r'^', include('userena.urls')),

)