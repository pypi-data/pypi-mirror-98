from django.test import TestCase
from cradmin_legacy import cradmin_testhelpers
from model_mommy import mommy

from devilry.devilry_admin.views.assignment import first_deadline


class TestOverviewAppUpdateFirstDeadline(TestCase, cradmin_testhelpers.TestCaseMixin):
    viewclass = first_deadline.AssignmentFirstDeadlineUpdateView

    def test_h1(self):
        assignment = mommy.make('core.Assignment')
        mockresponse = self.mock_http200_getrequest_htmls(cradmin_role=assignment, viewkwargs={'pk':assignment.id})
        self.assertEqual(mockresponse.selector.one('h1').alltext_normalized, 'Edit first deadline')
