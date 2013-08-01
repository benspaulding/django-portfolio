""" Simple urls for use in testing the portfolio app. """

from __future__ import unicode_literals

from django.conf.urls import include, patterns, url


urlpatterns = patterns('',
    url(r'^portfolio/', include('portfolio.urls')),
)
