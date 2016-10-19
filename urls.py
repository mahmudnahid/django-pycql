from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
                       url(r'^node/', include('node.urls')),
                       )

urlpatterns += staticfiles_urlpatterns()