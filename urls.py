from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import login, logout
from maths.centres.views import welcome
from maths.cat_test.views import start_test

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'maths.views.home', name='home'),
    # url(r'^maths/', include('maths.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    (r'^accounts/login/$',  login,  {'extra_context':{'next': '/welcome/'}}),
    (r'^accounts/logout/$', logout),
    (r'^welcome/$', welcome),
    (r'^start/$', start_test),	
)
