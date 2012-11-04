from django.test import TestCase
from django.utils import timezone

from ..models import _get_upload_to_path, Project


class PortfolioTestModel(PortfolioBase):
    """A concrete class solely for testing the PortfolioBase abstract model."""
    class Meta:
        # Must supply app_label so this gets added to the db correctly.
        app_label = PortfolioBase._meta.app_label


class MediaFuncTestCase(TestCase):

    def test_project_file(self):
        project = Project(name=u'Proj 1', slug=u'proj-1')
        filepath = _get_upload_to_path(project, 'foo.png')
        self.assertEqual(filepath, 'img/portfolio/proj-1/foo.png')


class PortfolioBaseTestCase(TestCase):

    def test_get_absolute_url(self):
        """An odd test case, but necessary to verify current behavior."""
        from django.core.urlresolvers import NoReverseMatch
        obj = PortfolioTestModel(name=u'Foo', slug=u'foo')
        self.assertRaises(NoReverseMatch, obj.get_absolute_url)


class PortfolioTestCase(TestCase):

    def test_is_complete_past_date(self):
        past_date = timezone.datetime.date(timezone.now())
        proj_complete = Project(completion_date=past_date)
        self.assertTrue(proj_complete.is_complete())

    def test_is_complete_future_date(self):
        now = timezone.now()
        future_date = timezone.datetime.date(timezone.datetime(now.year+1, now.month, now.day))
        proj_incomplete = Project(completion_date=future_date)
        self.assertFalse(proj_incomplete.is_complete())

    def test_is_complete_null_date(self):
        proj_incomplete = Project(completion_date=None)
        self.assertFalse(proj_incomplete.is_complete())

    def test_in_development_ongoing(self):
        proj_ongoing = Project(is_ongoing=True)
        self.assertTrue(proj_ongoing.in_development())

    def test_in_development_complete(self):
        past_date = timezone.datetime.date(timezone.now())
        proj_complete = Project(completion_date=past_date)
        self.assertFalse(proj_complete.in_development())

    def test_in_development_ongoing_complete(self):
        """
        This tests an illogical case, but is needed to verify current behavior.
        """
        proj_ongoing_complete = Project(is_ongoing=True,
                                        completion_date=timezone.now())
        self.assertTrue(proj_ongoing_complete.in_development())
