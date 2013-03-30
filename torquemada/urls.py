from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'questions.views.home', name='home'),
    url(r'^vote/(?P<pk>[^\.]+)/(?P<verb>[^\.]+)/$', 'questions.views.vote', name='vote'),
    url(r'^cancel_vote/(?P<pk>[^\.]+)/$', 'questions.views.cancel_vote', name='cancel_vote'),
	url(r'^ask/$', 'questions.views.ask', name='ask'),
    # url(r'^torquemada/', include('torquemada.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
