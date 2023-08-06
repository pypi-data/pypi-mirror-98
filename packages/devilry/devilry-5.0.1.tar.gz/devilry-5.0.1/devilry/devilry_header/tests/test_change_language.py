from django.test import TestCase
from django.urls import reverse

from devilry.project.develop.testhelpers.corebuilder import UserBuilder
from devilry.project.develop.testhelpers.login import LoginTestCaseMixin


class TestChangeLanguage(TestCase, LoginTestCaseMixin):
    def setUp(self):
        self.url = reverse('devilry_change_language')

    def test_not_authenticated(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

    def test_post_valid(self):
        testuser = UserBuilder('testuser')
        testuser.update(
            languagecode='nb'
        )
        with self.settings(LANGUAGES=[('en', 'English')]):
            response = self.post_as(testuser.user, self.url, {
                'languagecode': 'en',
                'redirect_url': '/successtest'
            })
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response['Location'], '/successtest')
            testuser.reload_from_db()
            self.assertEqual(testuser.user.languagecode, 'en')

    def test_post_invalid(self):
        testuser = UserBuilder('testuser')
        testuser.update(
            languagecode='nb'
        )
        with self.settings(LANGUAGES=[('en', 'English')]):
            response = self.post_as(testuser.user, self.url, {
                'languagecode': 'tu',
                'redirect_url': '/successtest'
            })
            self.assertEqual(response.status_code, 400)
            testuser.reload_from_db()
            self.assertEqual(testuser.user.languagecode, 'nb')
