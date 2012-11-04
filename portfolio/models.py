from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from portfolio import constants


# Helper functions

def _get_upload_to_path(instance, filename):
    """
    Returns an upload path using the instance slug.

    This function keeps file uploads organized.
    """
    return "img/portfolio/%s/%s" % (instance.slug, filename)


# Fields

class StatusField(models.PositiveSmallIntegerField):
    """Model field for the pubishing status of an object."""

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = kwargs.get('choices', constants.STATUS_CHOICES)
        kwargs['db_index'] = kwargs.get('db_index', True)
        kwargs['default'] = kwargs.get('default', constants.DRAFTED)
        models.PositiveSmallIntegerField.__init__(self, *args, **kwargs)


# Managers

class StatusManager(models.Manager):
    """A manager for models with a `StatusField`."""

    def drafted(self):
        """Return only objects which are drafted."""
        return self.get_query_set().filter(status=constants.DRAFTED)

    def published(self):
        """Return only objects which are published."""
        return self.get_query_set().filter(status=constants.PUBLISHED)

    def removed(self):
        """Return only objects which are removed from publich view."""
        return self.get_query_set().filter(status=constants.REMOVED)


# Models

class PortfolioBase(models.Model):
    """Base class with fields and methods common to all Portfolio models."""

    name = models.CharField(_(u'name'), max_length=255, unique=True)
    slug = models.SlugField(_(u'slug'), unique=True)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    # NOTE: I was trying to be Super Helpful (TM) when I wrote this, but it
    # is silly. It adds a ``get_absolute_url`` method for all subclasses, even
    # though not one of those has a detail view at this time. And it makes the
    # assumption that the url will be named based on the class name. That is
    # common, but not always the case. This stays for backward compatibility.
    @models.permalink
    def get_absolute_url(self):
        return ('portfolio-%s-detail' % self.__class__.__name__.lower(), (),
            {'slug': self.slug})


class Client(PortfolioBase):
    """A client in the portfolio."""

    url = models.URLField(_(u'URL'), blank=True)

    class Meta(PortfolioBase.Meta):
        verbose_name = _(u'client')
        verbose_name_plural = _(u'clients')


class Testimonial(models.Model):
    """A testimonial as given by a ``Client``."""
    client = models.ForeignKey(Client, verbose_name=_(u'client'),
        related_name='testimonials')
    witness = models.CharField(_(u'witness'), max_length=255, blank=True)
    witness_desc = models.CharField(_(u'witness\' position'), max_length=255,
        blank=True, help_text=_(u'Describe their position or relationship.'))
    date = models.DateField(_(u'date'))
    testimonial = models.TextField(_(u'testimonial'))
    status = StatusField(_(u'status'))

    objects = StatusManager()

    class Meta:
        ordering = ('-date',)
        verbose_name = _(u'testimonial')
        verbose_name_plural = _(u'testimonials')

    def __unicode__(self):
        return self.witness


class Medium(PortfolioBase):
    """Different media that projects are created in."""

    class Meta(PortfolioBase.Meta):
        verbose_name = _(u'medium')
        verbose_name_plural = _(u'media')


class Discipline(PortfolioBase):
    """Different disciplines practiced within a project."""

    class Meta(PortfolioBase.Meta):
        verbose_name = _(u'discipline')
        verbose_name_plural = _(u'disciplines')


class Project(PortfolioBase):
    """A project in the portfolio."""

    project_url = models.URLField(_(u'project URL'))
    completion_date = models.DateField(_(u'completion date'),
        blank=True, null=True)
    is_ongoing = models.BooleanField(_(u'is ongoing'))

    summary = models.TextField(_(u'summary'), blank=True)
    description = models.TextField(_(u'description'))
    client = models.ForeignKey(Client, verbose_name=_(u'client'),
        related_name='projects')
    overview_image = models.ImageField(_(u'overview image'), blank=True,
        upload_to=_get_upload_to_path)
    detail_image = models.ImageField(_(u'detail image'), blank=True,
        upload_to=_get_upload_to_path)

    media = models.ManyToManyField(Medium, verbose_name=_(u'media'),
        related_name='projects')
    disciplines = models.ManyToManyField(Discipline,
        verbose_name=_(u'disciplines'), related_name='projects')
    status = StatusField(_(u'status'))

    objects = StatusManager()

    class Meta:
        get_latest_by = 'completion_date'
        # FIXME: The ordering of these will be non-deterministic, because the
        # ``completion_date`` is nullable. (Some DB's pile null dates at the
        # end, some at the beginning. I did not know that when I originally
        # wrote the app.) So, rework date handling and ordering to get
        # a deterministic ordering.
        ordering = ('-completion_date', 'name')
        verbose_name = _(u'project')
        verbose_name_plural = _(u'projects')

    def is_complete(self):
        """Returns True if completion date is earlier than current time."""
        if not self.completion_date:
            return False
        return self.completion_date <= timezone.datetime.date(timezone.now())
    is_complete.boolean = True
    is_complete.short_description = _(u'is complete')

    def in_development(self):
        """Returns True if completion date is later than current time."""
        return self.is_ongoing or not self.is_complete()
    in_development.boolean = True
    in_development.short_description = _(u'in development')
