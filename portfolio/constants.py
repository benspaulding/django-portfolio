from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _


# Status constants
DRAFTED = 1
PUBLISHED = 2
REMOVED = 3

STATUS_CHOICES = (
    (DRAFTED, _('drafted')),
    (PUBLISHED, _('published')),
    (REMOVED, _('removed')),
)
