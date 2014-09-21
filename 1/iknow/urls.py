from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from views import index

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'xs7.views.home', name='home'),
    # url(r'^xs7/', include('xs7.foo.urls')),
    url(r'^$', index),
)
