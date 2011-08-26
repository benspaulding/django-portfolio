# -*- coding: utf-8 -*-

"""
Models for a portfolio application.

"""

import re
import datetime

from django.conf import settings
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from template_utils.markup import formatter
from tagging.fields import TagField

from portfolio import managers



class Client(models.Model):
    """
    A client in the portfolio.
    
    """
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, _(u'Live')),
        (DRAFT_STATUS, _(u'Draft')),
        (HIDDEN_STATUS, _(u'Hidden')),
    )
    name = models.CharField(_(u'name'), max_length=250, unique=True)
    slug = models.SlugField(_(u'slug'), unique=True)
    url = models.URLField(_(u'URL'), blank=True)
    status = models.IntegerField(_(u'status'), choices=STATUS_CHOICES, default=DRAFT_STATUS, help_text=_(u'Only clients with “Live” status will be displayed publicly.'))
    
    # Managers
    objects = models.Manager()
    live = managers.LiveItemManager()
    
    class Meta:
        ordering = ['name']
        verbose_name = _(u'client')
        verbose_name_plural = _(u'clients')
        
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return ('django.views.generic.list_detail.object_detail', [str(self.slug)])
    get_absolute_url = permalink(get_absolute_url)
    
    def get_next(self):
        try:
            return Client.objects.filter(status__exact=LIVE_STATUS).filter(name__gt=self.name)[0]
        except IndexError:
            return None
    
    def get_previous(self):
        try:
            return Client.objects.filter(status__exact=LIVE_STATUS).filter(name__lt=self.name).order_by('-name')[0]
        except IndexError:
            return None
        

class Testimonial(models.Model):
    """
    A testimonial as given by a ``Client``
    
    """
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, _(u'Live')),
        (DRAFT_STATUS, _(u'Draft')),
        (HIDDEN_STATUS, _(u'Hidden')),
    )
    client = models.ForeignKey(Client, verbose_name=_(u'client'), related_name='testimonials')
    witness = models.CharField(_(u'witness'), max_length=250, blank=True)
    witness_desc = models.CharField(_(u'witness’ position'), max_length=250, blank=True, help_text=_(u'May be a position or relationship.'))
    date = models.DateField(_(u'date'),)
    testimonial = models.TextField(_(u'testimonial'),)
    status = models.IntegerField(_(u'status'), choices=STATUS_CHOICES, help_text=_(u'Only testimonials with “Live” status will be displayed publicly.'))
    
    # Managers
    objects = models.Manager()
    live = managers.LiveItemManager()
    
    class Meta:
        ordering = ['-date']
        verbose_name = _(u'testimonial')
        verbose_name_plural = _(u'testimonials')
        
    def __unicode__(self):
        return self.witness


class Medium(models.Model):
    """
    Different media that projects are created in.
    
    """
    name = models.CharField(_(u'name'), max_length=250, unique=True)
    slug = models.SlugField(_(u'slug'), unique=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = _(u'medium')
        verbose_name_plural = _(u'media')
    
    class Admin:
        list_display = ('name',)
        list_per_page = 50;
        search_fields = ['name',]
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return ('django.views.generic.list_detail.object_detail', [str(self.slug)])
    get_absolute_url = permalink(get_absolute_url)
    
    def get_next(self):
        try:
            return Medium.objects.filter(name__gt=self.name)[0]
        except IndexError:
            return None
    
    def get_previous(self):
        try:
            return Medium.objects.filter(name__lt=self.name).order_by('-name')[0]
        except IndexError:
            return None



class Discipline(models.Model):
    """
    Different disciplines practiced within a ``Project``
    
    """
    name = models.CharField(_(u'name'), max_length=250, unique=True)
    slug = models.SlugField(_(u'slug'), unique=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = _(u'discipline')
        verbose_name_plural = _(u'disciplines')
        
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return ('django.views.generic.list_detail.object_detail', [str(self.slug)])
    get_absolute_url = permalink(get_absolute_url)
    
    def get_next(self):
        try:
            return Discipline.objects.filter(name__gt=self.name)[0]
        except IndexError:
            return None
    
    def get_previous(self):
        try:
            return Discipline.objects.filter(name__lt=self.name).order_by('-name')[0]
        except IndexError:
            return None


class Project(models.Model):
    """
    An project in the portfolio.
    
    Slightly denormalized, because it uses two fields the description: 
    one for the actual text the user types in, and another to store 
    the HTML version of the Project (e.g., as generated by a text-to-HTML 
    converter like Textile or Markdown). This saves having to run the 
    conversion each time the Project is displayed.
    
    """
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, _(u'Live')),
        (DRAFT_STATUS, _(u'Draft')),
        (HIDDEN_STATUS, _(u'Hidden')),
    )
    
    # Metadata
    name = models.CharField(_(u'name'), max_length=250, unique=True)
    slug = models.SlugField(_(u'slug'), unique=True)
    project_url = models.URLField(_(u'project URL'))
    completion_date = models.DateField(_(u'completion date'))
    in_development = models.BooleanField(_(u'in development'))
    status = models.IntegerField(_(u'status'), choices=STATUS_CHOICES, default=DRAFT_STATUS, help_text=_(u'Only projects with “Live” status will be displayed publicly.'))
    
    # The actual Project bits
    summary_txt = models.TextField(_(u'summary'), blank=True, help_text=_(u'Markdown syntax allowed.'))
    summary_xml = models.TextField(_(u'summary as HTML'), editable=False, blank=True, null=True)
    description_txt = models.TextField(_(u'description'), help_text=_(u'Markdown syntax allowed.'))
    description_xml = models.TextField(_(u'description as HTML'), editable=False, blank=True)
    client = models.ForeignKey(Client, verbose_name=_(u'client'), related_name='projects')
    overview_image = models.ImageField(_(u'overview image'), upload_to='img/portfolio/', height_field='height', width_field='width', blank=True)
    detail_image = models.ImageField(_(u'detail image'), upload_to='img/portfolio/', height_field='height', width_field='width', blank=True)
    
    # Categorization
    media = models.ManyToManyField(Medium, verbose_name=_(u'media'), related_name='projects')
    disciplines = models.ManyToManyField(Discipline, verbose_name=_(u'disciplines'), related_name='projects')
    tags = TagField(_(u'tags'), help_text=_(u'oneword, lowercase, commaseperated'), blank=True)
    
    # Managers
    objects = models.Manager()
    live = managers.LiveItemManager()
    
    class Meta:
        ordering = ['-completion_date']
        verbose_name = _(u'project')
        verbose_name_plural = _(u'projects')
        
    def __unicode__(self):
        return self.name

    def save(self):
        if self.summary_txt:
            self.summary_xml = formatter(self.summary_txt)
        self.description_xml = formatter(self.description_txt)
        super(Project, self).save()
    
    def get_absolute_url(self):
        return ('django.views.generic.list_detail.object_detail', [str(self.slug)])
    get_absolute_url = permalink(get_absolute_url)
    
    def get_next(self):
        try:
            return Project.objects.filter(status__exact=LIVE_STATUS).filter(name__gt=self.name)[0]
        except IndexError:
            return None
    
    def get_previous(self):
        try:
            return Project.objects.filter(status__exact=LIVE_STATUS).filter(name__lt=self.name).order_by('-name')[0]
        except IndexError:
            return None
