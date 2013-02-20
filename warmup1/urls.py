from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'warmup1.views.home', name='home'),
    # url(r'^warmup1/', include('warmup1.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),             
    url(r'^$', 'users.models.client'),
    url(r'^users/login$', 'users.models.login'),
    url(r'^users/add$', 'users.models.add'),
    url(r'^TESTAPI/resetFixture$', 'users.models.TESTAPI_resetFixture'),
    url(r'^TESTAPI/unitTests$', 'users.models.TESTAPI_unitTests'),
)
urlpatterns += staticfiles_urlpatterns()
