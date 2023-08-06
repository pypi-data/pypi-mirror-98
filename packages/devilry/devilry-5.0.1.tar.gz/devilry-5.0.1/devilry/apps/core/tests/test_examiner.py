from django import test
from model_mommy import mommy


class TestExaminerModel(test.TestCase):
    def test_get_anonymous_name_with_anonymous_id(self):
        examiner = mommy.make('core.Examiner',
                              relatedexaminer__automatic_anonymous_id='MyAutomaticID')
        self.assertEqual('MyAutomaticID', examiner.get_anonymous_name())

    def test_get_anonymous_name_no_anonymous_id(self):
        examiner = mommy.make('core.Examiner',
                              relatedexaminer__automatic_anonymous_id='')
        self.assertEqual('Automatic anonymous ID missing', examiner.get_anonymous_name())
