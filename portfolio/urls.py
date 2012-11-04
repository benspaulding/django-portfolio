from django.conf.urls.defaults import *
from django.views.generic.list import ListView

from .models import Project


urlpatterns = patterns('',
    url(r'^$',
        ListView.as_view(context_object_name='project',
                         queryset=Project.objects.published()),
        name='portfolio-project-list'),
)
