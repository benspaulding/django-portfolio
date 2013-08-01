""" Simple urls for use in testing the portfolio app. """

from django.conf.urls import include, patterns, url


urlpatterns = patterns('',
    url(r'^portfolio/', include('portfolio.urls')),
)
