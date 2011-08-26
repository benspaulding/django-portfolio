# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.views.generic.list_detail import *

from portfolio.models import Project
	
info_dict = {
    'queryset': Project.live.all(),
    'template_object_name': 'project',
}

urlpatterns = patterns('',
    url(r'^$', 
        object_list, 
        info_dict, 
        name='portfolio_project_list'),
)
