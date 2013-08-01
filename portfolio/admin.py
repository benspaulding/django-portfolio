from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop, ungettext

from .constants import STATUS_CHOICES, DRAFTED, PUBLISHED, REMOVED
from .models import Client, Testimonial, Medium, Discipline, Project


def update_status(modeladmin, request, queryset, status):
    """The workhorse function for the admin action functions that follow."""
    # We loop over the objects here rather than use queryset.update() for
    # two reasons:
    #
    #  1. No one should ever be updating zillions of portfolio objects, so
    #     performance is not an issue.
    #  2. To be tidy, we want to log what the user has done.
    #
    for obj in queryset:
        obj.status = status
        obj.save()
        # Now log what happened.
        # Use ugettext_noop() 'cause this is going straight into the db.
        log_message = ugettext_noop(u'Changed status to \'%s\'.' %
            obj.get_status_display())
        modeladmin.log_change(request, obj, log_message)

    # Send a message to the user telling them what has happened.
    message_dict = {
        'count': queryset.count(),
        'object': modeladmin.model._meta.verbose_name,
        'verb': dict(STATUS_CHOICES)[status],
    }
    if not message_dict['count'] == 1:
        message_dict['object'] = modeladmin.model._meta.verbose_name_plural
    user_message = ungettext(
        u'%(count)s %(object)s was successfully %(verb)s.',
        u'%(count)s  %(object)s were successfully %(verb)s.',
        message_dict['count']) % message_dict
    modeladmin.message_user(request, user_message)

    # Return None to display the change list page again and allow the user
    # to reload the page without getting that nasty "Send the form again ..."
    # warning from their browser.
    return None


def draft(modeladmin, request, queryset):
    """Admin action for setting status of selected items to 'drafted'."""
    return update_status(modeladmin, request, queryset, DRAFTED)
draft.short_description = _(u'Draft selected %(verbose_name_plural)s')


def publish(modeladmin, request, queryset):
    """Admin action for setting status of selected items to 'published'."""
    return update_status(modeladmin, request, queryset, PUBLISHED)
publish.short_description = _(u'Publish selected %(verbose_name_plural)s')


def remove(modeladmin, request, queryset):
    """Admin action for setting status of selected items to 'removed'."""
    return update_status(modeladmin, request, queryset, REMOVED)
remove.short_description = _(u'Remove selected %(verbose_name_plural)s')


class TestimonialInline(admin.StackedInline):
    extra = 1
    model = Testimonial


class PortfolioBaseAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_per_page = 50
    prepopulated_fields = {'slug': ('name', )}
    search_fields = ('name', )


class ClientAdmin(PortfolioBaseAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'url')}),
    )
    inlines = (TestimonialInline, )
    list_display = ('name', 'url')
    search_fields = ('name', 'url')


class ProjectAdmin(PortfolioBaseAdmin):
    actions = (draft, publish, remove)
    date_hierarchy = 'completion_date'
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'client', 'project_url',
            ('completion_date', 'is_ongoing'), 'status')}),
        (_(u'Content'), {'fields': ('summary', 'description', 'overview_image',
            'detail_image')}),
        (_(u'Categorization'), {'fields': ('media', 'disciplines')}),
    )
    filter_horizontal = ('disciplines', )
    list_display = ('name', 'client', 'completion_date', 'status',
        'in_development')
    list_filter = ('status', 'completion_date', 'is_ongoing', 'media',
        'disciplines')
    search_fields = ('name', 'summary', 'description')


admin.site.register(Medium, PortfolioBaseAdmin)
admin.site.register(Discipline, PortfolioBaseAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Project, ProjectAdmin)
