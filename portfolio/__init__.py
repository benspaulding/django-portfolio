# Mark the app_label for translation. Use try/except to avoid ``ImportError``
# when setup imports version before Django is installed.
try:
    from django.utils.translation import ugettext_lazy as _
    _(u'portfolio')
except ImportError:
    pass
