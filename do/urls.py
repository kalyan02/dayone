from django.conf.urls import patterns, include, url
from social_auth.views import auth as sn_auth, complete as sn_complete, disconnect as sn_disconnect
import do.views.simple, do.views.profile
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', do.views.simple.main, name='index' ),
    url(r'^home', do.views.simple.main ),
    url(r'^auth_ok', do.views.simple.login_ok ),

	url(r'^login/(?P<backend>[^/]+)/$', sn_auth, name='socialauth_begin'), 
	url(r'^login/complete/(?P<backend>[^/]+)/$', sn_complete, name='socialauth_complete'),

	url(r'^auth_complete$', do.views.profile.auth_complete, name='auth_complete'),
	url(r'^setup_profile$', do.views.profile.setup_profile, name='setup_profile'),
	url(r'^edit_profile$', do.views.profile.edit_profile, name='edit_profile'),
	url(r'^api_profile$', do.views.profile.api_profile, name='api_profile'),
	url(r'^entries$', do.views.profile.view_entries, name='view_entries'),
	url(r'^entries_refresh$', do.views.profile.entries_refresh, name='entries_refresh')

	# # XXX: Deprecated, this URLs are deprecated, instead use the login and
	# #      complete ones directly, they will differentiate the user intention
	# #      by checking it's authenticated status association.
	# url(r'^accounts/associate/(?P<backend>[^/]+)/$', sn_auth, name='socialauth_associate_begin'),
	# url(r'^accounts/associate/complete/(?P<backend>[^/]+)/$', sn_complete, name='socialauth_associate_complete'),

	# # disconnection
	# url(r'^accounts/disconnect/(?P<backend>[^/]+)/$', sn_disconnect, name='socialauth_disconnect'),
	# url(r'^accounts/disconnect/(?P<backend>[^/]+)/(?P<association_id>[^/]+)/$', sn_disconnect, name='socialauth_disconnect_individual'),
)
