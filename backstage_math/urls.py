from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from backstage_math.views import DifferentialHome, DifferentialView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'backstage_math.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', DifferentialHome.as_view()),
    url(r'^difference/', DifferentialView.as_view()),
) 

urlpatterns += staticfiles_urlpatterns()