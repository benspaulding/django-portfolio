from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .constants import STATUS_CHOICES, DRAFTED, PUBLISHED, REMOVED


# Helper functions

def _get_upload_to_path(instance, filename):
    """
    Returns an upload path using the instance slug.

    This function keeps file uploads organized.
    """
    import posixpath
    return "img/portfolio/%s/%s" % (instance.slug, filename)


# Fields
# South migrations are provided, and thus an introspection rule for the
# StatusField. But South is an option, not a requirement, so a try/except is
# necessary.
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^portfolio\.models\.StatusField'])
except ImportError:
    pass


class StatusField(models.PositiveSmallIntegerField):
    """Model field for the pubishing status of an object."""

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = kwargs.get('choices', STATUS_CHOICES)
        kwargs['db_index'] = kwargs.get('db_index', True)
        kwargs['default'] = kwargs.get('default', DRAFTED)
        models.PositiveSmallIntegerField.__init__(self, *args, **kwargs)


# Managers

class StatusManager(models.Manager):
    """A manager for models with a `StatusField`."""

    def drafted(self):
        """Return only objects which are drafted."""
        return self.get_query_set().filter(status=DRAFTED)

    def published(self):
        """Return only objects which are published."""
        return self.get_query_set().filter(status=PUBLISHED)

    def removed(self):
        """Return only objects which are removed from publich view."""
        return self.get_query_set().filter(status=REMOVED)


# Models

@python_2_unicode_compatible
class PortfolioBase(models.Model):
    """Base class with fields and methods common to all Portfolio models."""

    name = models.CharField(_('name'), max_length=255, unique=True)
    slug = models.SlugField(_('slug'), unique=True)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name

    # NOTE: I was trying to be Super Helpful (TM) when I wrote this, but it
    # is silly. It adds a ``get_absolute_url`` method for all subclasses, even
    # though not one of those has a detail view at this time. And it makes the
    # assumption that the url will be named based on the class name. That is
    # common, but not always the case. This stays for backward compatibility.
    def get_absolute_url(self):
        return reverse('portfolio-%s-detail' % self.__class__.__name__.lower(),
            args=(), kwargs={'slug': self.slug})


class Client(PortfolioBase):
    """A client in the portfolio."""

    url = models.URLField(_('URL'), blank=True)

    class Meta(PortfolioBase.Meta):
        verbose_name = _('client')
        verbose_name_plural = _('clients')


class Testimonial(models.Model):
    """A testimonial as given by a ``Client``."""
    client = models.ForeignKey(Client, verbose_name=_('client'),
        related_name='testimonials')
    witness = models.CharField(_('witness'), max_length=255, blank=True)
    witness_desc = models.CharField(_('witness\' position'), max_length=255,
        blank=True, help_text=_('Describe their position or relationship.'))
    date = models.DateField(_('date'))
    testimonial = models.TextField(_('testimonial'))
    status = StatusField(_('status'))

    objects = StatusManager()

    class Meta:
        ordering = ('-date',)
        verbose_name = _('testimonial')
        verbose_name_plural = _('testimonials')

    def __str__(self):
        return self.witness


class Medium(PortfolioBase):
    """Different media that projects are created in."""

    class Meta(PortfolioBase.Meta):
        verbose_name = _('medium')
        verbose_name_plural = _('media')


class Discipline(PortfolioBase):
    """Different disciplines practiced within a project."""

    class Meta(PortfolioBase.Meta):
        verbose_name = _('discipline')
        verbose_name_plural = _('disciplines')


class Project(PortfolioBase):
    """A project in the portfolio."""

    project_url = models.URLField(_('project URL'))
    completion_date = models.DateField(_('completion date'),
        blank=True, null=True)
    is_ongoing = models.BooleanField(_('is ongoing'))

    summary = models.TextField(_('summary'), blank=True)
    description = models.TextField(_('description'))
    client = models.ForeignKey(Client, verbose_name=_('client'),
        related_name='projects')
    overview_image = models.ImageField(_('overview image'), blank=True,
        upload_to=_get_upload_to_path)
    detail_image = models.ImageField(_('detail image'), blank=True,
        upload_to=_get_upload_to_path)

    media = models.ManyToManyField(Medium, verbose_name=_('media'),
        related_name='projects')
    disciplines = models.ManyToManyField(Discipline,
        verbose_name=_('disciplines'), related_name='projects')
    status = StatusField(_('status'))

    objects = StatusManager()

    class Meta:
        get_latest_by = 'completion_date'
        # FIXME: The ordering of these will be non-deterministic, because the
        # ``completion_date`` is nullable. (Some DB's pile null dates at the
        # end, some at the beginning. I did not know that when I originally
        # wrote the app.) So, rework date handling and ordering to get
        # a deterministic ordering.
        ordering = ('-completion_date', 'name')
        verbose_name = _('project')
        verbose_name_plural = _('projects')

    def is_complete(self):
        """Returns True if completion date is earlier than current time."""
        if not self.completion_date:
            return False
        return self.completion_date <= timezone.datetime.date(timezone.now())
    is_complete.boolean = True
    is_complete.short_description = _('is complete')

    def in_development(self):
        """Returns True if completion date is later than current time."""
        return self.is_ongoing or not self.is_complete()
    in_development.boolean = True
    in_development.short_description = _('in development')
