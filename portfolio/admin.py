"""
Django admin models for a portfolio application.

"""

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from portfolio.models import *


class TestimonialInline(admin.TabularInline):
    model = Testimonial
    extra = 2

class ClientAdmin(admin.ModelAdmin):
    fieldsets = (
        (_(u'Client Information'), {'fields': (('name', 'slug'), 'url', 'status',)}),
    )
    inlines = [ TestimonialInline, ]
    list_display = ('name', 'url', 'status')
    list_filter = ['status',]
    list_per_page = 50
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'url']
    

class MediumAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_per_page = 50
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name',]
    

class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_per_page = 50
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name',]
    

class ProjectAdmin(admin.ModelAdmin):
    date_hierarchy = 'completion_date'
    fieldsets = (
        (_(u'Metadata'), {'fields': (('name', 'slug'), 'client', 'project_url', 'completion_date', 'in_development', 'status',) }),
        (_(u'Project'), {'fields': ('summary_txt', 'description_txt', 'overview_image', 'detail_image',) }),
        (_(u'Categorization'), {'fields': ('media', 'disciplines', 'tags',) }),
    )
    filter_horizontal = ('disciplines',)
    list_display = ('name', 'client', 'completion_date', 'status')
    list_filter = ['status', 'media', 'disciplines',]
    list_per_page = 50
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'summary_txt', 'description_txt']
    

admin.site.register(Client, ClientAdmin)
admin.site.register(Medium, MediumAdmin)
admin.site.register(Discipline, DisciplineAdmin)
admin.site.register(Project, ProjectAdmin)
