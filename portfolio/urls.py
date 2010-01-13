from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list

from portfolio.models import Project


info_dict = {
    'queryset': Project.objects.published(),
    'template_object_name': 'project',
}

urlpatterns = patterns('',
    url(r'^$', object_list, info_dict, name='portfolio-project-list'),
)
