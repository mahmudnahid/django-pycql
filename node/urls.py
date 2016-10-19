from django.conf.urls import patterns, url

urlpatterns = patterns('node.views',
                       url(r'^add/$', 'node_add', name='node_add'),
                       url(r'^edit/(?P<pk>[A-Za-z0-9-]+)/$', 'node_edit', name='node_edit'),
                       url(r'^delete/(?P<pk>[A-Za-z0-9-]+)/$', 'node_delete', name='node_delete'),
                       url(r'^detail/(?P<pk>[A-Za-z0-9-]+)/$', 'node_detail', name='node_detail'),
                       url(r'^index/$', 'node_index', name='node_index'),
                       )