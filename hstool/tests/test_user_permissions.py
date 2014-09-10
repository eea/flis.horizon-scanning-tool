from django.core.urlresolvers import reverse
from django_webtest import WebTest

from .factories import (
    UserFactory,
)


class AuthenticatedListViewTests(WebTest):
    def setUp(self):
        self.user = UserFactory(username='username')

    def test_assessments_authenticated(self):
        url = reverse('home_view')
        resp = self.app.get(url, user=self.user)
        self.assertEqual(resp.status_code, 200)

    def test_drivers_authenticated(self):
        url = reverse('drivers:list')
        resp = self.app.get(url, user=self.user)
        self.assertEqual(resp.status_code, 200)

    def test_indicators_authenticated(self):
        url = reverse('indicators:list')
        resp = self.app.get(url, user=self.user)
        self.assertEqual(resp.status_code, 200)

    def test_sources_authenticated(self):
        url = reverse('sources:list')
        resp = self.app.get(url, user=self.user)
        self.assertEqual(resp.status_code, 200)

    def test_figures_authenticated(self):
        url = reverse('figures:list')
        resp = self.app.get(url, user=self.user)
        self.assertEqual(resp.status_code, 200)


class AnonymousListViewTests(WebTest):
    def setUp(self):
        self.user = UserFactory(username='username')

    def test_assessments_not_authenticated(self):
        url = reverse('home_view')
        resp = self.app.get(url, expect_errors=True)
        self.assertEqual(resp.status_code, 403)

    def test_drivers_not_authenticated(self):
        url = reverse('drivers:list')
        resp = self.app.get(url, expect_errors=True)
        self.assertEqual(resp.status_code, 403)

    def test_indicators_not_authenticated(self):
        url = reverse('indicators:list')
        resp = self.app.get(url, expect_errors=True)
        self.assertEqual(resp.status_code, 403)

    def test_sources_not_authenticated(self):
        url = reverse('sources:list')
        resp = self.app.get(url, expect_errors=True)
        self.assertEqual(resp.status_code, 403)

    def test_figures_not_authenticated(self):
        url = reverse('figures:list')
        resp = self.app.get(url, expect_errors=True)
        self.assertEqual(resp.status_code, 403)


class AuthenticatedAddViewTests(WebTest):
    def setUp(self):
        self.user = UserFactory(username='username')

    def test_assessments_authenticated(self):
        url = reverse('assessments:add')
        resp = self.app.get(url, user=self.user)
        self.assertEqual(resp.status_code, 200)

    def test_drivers_authenticated(self):
        url = reverse('drivers:add')
        resp = self.app.get(url, user=self.user)
        self.assertEqual(resp.status_code, 200)

    def test_indicators_authenticated(self):
        url = reverse('indicators:add')
        resp = self.app.get(url, user=self.user)
        self.assertEqual(resp.status_code, 200)

    def test_sources_authenticated(self):
        url = reverse('sources:add')
        resp = self.app.get(url, user=self.user)
        self.assertEqual(resp.status_code, 200)

    def test_figures_authenticated(self):
        url = reverse('figures:add')
        resp = self.app.get(url, user=self.user)
        self.assertEqual(resp.status_code, 200)


class AnonymousAddViewTests(WebTest):
    def setUp(self):
        self.user = UserFactory(username='username')

    def test_assessments_not_authenticated(self):
        url = reverse('assessments:add')
        resp = self.app.get(url, expect_errors=True)
        self.assertEqual(resp.status_code, 403)

    def test_drivers_not_authenticated(self):
        url = reverse('drivers:add')
        resp = self.app.get(url, expect_errors=True)
        self.assertEqual(resp.status_code, 403)

    def test_indicators_not_authenticated(self):
        url = reverse('indicators:add')
        resp = self.app.get(url, expect_errors=True)
        self.assertEqual(resp.status_code, 403)

    def test_sources_not_authenticated(self):
        url = reverse('sources:add')
        resp = self.app.get(url, expect_errors=True)
        self.assertEqual(resp.status_code, 403)

    def test_figures_not_authenticated(self):
        url = reverse('figures:add')
        resp = self.app.get(url, expect_errors=True)
        self.assertEqual(resp.status_code, 403)
