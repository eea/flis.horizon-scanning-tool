from django.core.urlresolvers import reverse

from hstool.models import Implication
from .factories import (
    UserFactory, ImplicationFactory, GeoScopeFactory
)
from . import HSWebTest

REQUIRED = ['This field is required.']
REQUIRED_COUNTRY = ['The selected Geographical Scale requires a country.']


class ImplicationsAdd(HSWebTest):
    def setUp(self):
        GeoScopeFactory(title="EU Country", require_country=True)
        GeoScopeFactory(title="Beyond Europe", require_country=False)
        user = UserFactory(is_superuser=True)
        url = reverse('implications:add')
        self.resp = self.app.get(url, user=user)

    def test_default_fields_required(self):
        form = self.resp.forms[0]
        resp = form.submit()
        self.assertFormError(resp, 'form', 'title', REQUIRED)
        self.assertFormError(resp, 'form', 'policy_area', [])
        self.assertFormError(resp, 'form', 'description', REQUIRED)
        self.assertFormError(resp, 'form', 'geographical_scope', [])
        self.assertFormError(resp, 'form', 'sources', [])

    def test_successfully_added_no_country_required(self):
        form = self.resp.forms[0]
        form['title'] = 'title'
        form['policy_area'].select(text='Mock policy')
        form['description'] = 'description'
        form['geographical_scope'].select(text='Beyond Europe')
        resp = form.submit()
        self.assertRedirects(resp, reverse('implications:list'))
        self.assertEqual(len(Implication.objects.all()), 1)


    def test_successfully_added_country_required(self):
        form = self.resp.forms[0]
        form['title'] = 'title'
        form['policy_area'].select(text='Mock policy')
        form['description'] = 'description'
        form['geographical_scope'].select(text='EU Country')
        resp = form.submit()
        self.assertFormError(resp, 'form', 'country', REQUIRED_COUNTRY)


class ImplicationsUpdate(HSWebTest):
    def setUp(self):
        self.user = UserFactory()
        self.implication = ImplicationFactory(author_id=self.user.username)
        self.url = reverse('implications:update', args=(self.implication.pk, ))

    def test_existing_field_values(self):
        resp = self.app.get(self.url, user=self.user)
        form = resp.forms[0]
        self.assertEqual(form['title'].value, self.implication.title)
        self.assertEqual(form['description'].value, self.implication.description)

    def test_successfully_updated(self):
        resp = self.app.get(self.url, user=self.user)
        form = resp.forms[0]
        form['title'] = 'new_title'
        form['policy_area'].select(text='Mock policy')
        form['description'] = 'new_description'
        resp = form.submit()
        self.assertRedirects(resp, reverse('implications:list'))
        self.assertEqual(len(Implication.objects.all()), 1)
        implication = Implication.objects.first()
        self.assertEqual(implication.author_id, self.user.username)
        self.assertEqual(implication.title, 'new_title')
        self.assertEqual(implication.policy_area, 'mock_policy')
        self.assertEqual(implication.description, 'new_description')


class ImplicationsDelete(HSWebTest):
    def setUp(self):
        self.user = UserFactory()
        implication = ImplicationFactory(author_id=self.user.username)
        self.url = reverse('implications:delete', args=(implication.pk, ))

    def test_deletion(self):
        resp = self.app.get(self.url, user=self.user)
        self.form = resp.forms[0]
        resp = self.form.submit()
        self.assertRedirects(resp, reverse('implications:list'))
        self.assertQuerysetEqual(Implication.objects.all(), [])
