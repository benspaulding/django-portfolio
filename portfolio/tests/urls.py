""" Simple urls for use in testing the portfolio app. """

from django.conf.urls.defaults import include, patterns, url


urlpatterns = patterns('',
    url(r'^portfolio/', include('portfolio.urls')),
)
