from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('socialbooks.api.views',
                       url(r'^documents/$', 'main', {'SSL':True}, name="main"),
                       url(r'^documents/(?P<epub_id>\d+)/$', 'api_download', {'SSL':True}, name="api_download"),
                       url(r'^library(/?(?P<select>\w+)?)', 'library', name="api_library"),
                       url(r'^book/(?P<title>[^/]+)/(?P<key>\d+)/?', 'api_book', name='api_book'),
)			

urlpatterns += patterns('django.views.generic.simple',
                        url(r'^public/help/$', 'direct_to_template', {'template': 'api_help.html'}, name='api_help'),
                        )
