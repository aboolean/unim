from django.conf.urls import patterns, include, url
from rest_framework import routers
from android import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

router = routers.DefaultRouter()

# SET (AUTOMATIC) API URLS HERE
# router.register(r'locations', views.<SomeViewSet>)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'unim.views.home', name='home'),
    # url(r'^unim/', include('unim.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # REST API
    # url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^profile/$', views.profile),
    url(r'^state/$', views.state),
    url(r'^match/$', views.match),
    url(r'^cancel/$', views.cancel),
    url(r'^respond/$', views.respond),
    url(r'^rate/$', views.rate),
    url(r'^partner/$', views.partner),
    url(r'^$', views.api_root),
)
