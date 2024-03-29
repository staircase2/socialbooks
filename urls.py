from django.conf.urls.defaults import *
from django.contrib import admin

from django.conf import settings
from django.contrib.sitemaps import FlatPageSitemap

admin.autodiscover()

sitemaps = {
    'flatpages' : FlatPageSitemap,
}

urlpatterns = patterns('',

	(r'^%sadmin/(.*)' % settings.BASE_URL,  admin.site.root),
	(r'^%sr/' % settings.BASE_URL, include('django.conf.urls.shortcut')),
	
	# Sitemaps
	(r'^%ssitemap.xml$' % settings.BASE_URL, 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
	
	# Language setting
	(r'^%si18n/' % settings.BASE_URL, include('django.conf.urls.i18n')),
	
	# Auth
	(r'^%saccount/' % settings.BASE_URL, include('django_authopenid.urls')),                       
	
	# Library
	(r'^%s' % settings.BASE_URL, include('socialbooks.library.urls')),
	
	# Search 
	(r'^%ssearch/' % settings.BASE_URL, include('socialbooks.search.urls')),
	
	# API 
	(r'^api/', include('socialbooks.api.urls')),
)

if settings.DEBUG or settings.TESTING:
	urlpatterns += patterns('',
		#(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:-1], 'django.views.static.serve', {'document_root': settings.ROOT_PATH + '/library/templates/static'}),
		(r'^media/library/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.ROOT_PATH + '/library/templates/static'}),
		(r'^media/(?P<path>.+)$', 'django.views.static.serve', {'document_root': settings.ROOT_PATH + '/media'}),
		#(r'^orm-media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.ROOT_PATH + '/orm/templates/orm-media'}),
		(r'(?P<path>sitedown.html)$', 'django.views.static.serve', {'document_root': settings.ROOT_PATH + '/library/templates/'}),
	)