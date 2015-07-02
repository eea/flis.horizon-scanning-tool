from django.core.urlresolvers import reverse

from hstool.models import Impact
from .factories import (
    UserFactory, ImpactFactory, GeoScopeFactory, SourceFactory
)
from . import HSWebTest

REQUIRED = ['This field is required.']
REQUIRED_COUNTRY = ['The selected Geographical Scale requires a country.']


class ImpactsAdd(HSWebTest):
    def setUp(self):
        self.user = UserFactory(is_superuser=True)
        GeoScopeFactory(title="EU Country", require_country=True)
        GeoScopeFactory(title="Beyond Europe", require_country=False)
        SourceFactory(author_id=self.user.username)
        url = reverse('impacts:add')
        self.resp = self.app.get(url, user=self.user)

    def test_default_fields_required(self):
        form = self.resp.forms[0]
        resp = form.submit()
        self.assertFormError(resp, 'form', 'short_name', REQUIRED)
        self.assertFormError(resp, 'form', 'name', REQUIRED)
        self.assertFormError(resp, 'form', 'description', REQUIRED)
        self.assertFormError(resp, 'form', 'sources', [])

    def test_successfully_added_no_country_required(self):
        form = self.resp.forms[0]
        form['name'] = 'long name'
        form['short_name'] = 'short name'
        form['description'] = 'description'
        form['sources'] = '1'
        resp = form.submit()
        self.assertRedirects(resp, reverse('impacts:list'))
        self.assertEqual(len(Impact.objects.all()), 1)

    def test_successfully_added_country_required(self):
        form = self.resp.forms[0]
        form['name'] = 'long name'
        form['short_name'] = 'short name'
        form['description'] = 'description'
        form['sources'] = '1'
        form['geographical_scope'].select(text='EU Country')
        resp = form.submit()
        self.assertFormError(resp, 'form', 'country', REQUIRED_COUNTRY)


class ImpactsUpdate(HSWebTest):
    def setUp(self):
        self.user = UserFactory()
        self.impact = ImpactFactory(author_id=self.user.username)
        SourceFactory(author_id=self.user.username)
        self.url = reverse('impacts:update', args=(self.impact.pk, ))

    def test_existing_field_values(self):
        resp = self.app.get(self.url, user=self.user)
        form = resp.forms[0]
        self.assertEqual(form['name'].value, self.impact.name)
        self.assertEqual(form['short_name'].value, self.impact.short_name)
        self.assertEqual(form['description'].value, self.impact.description)

    def test_successfully_updated(self):
        resp = self.app.get(self.url, user=self.user)
        form = resp.forms[0]
        form['name'] = 'new_name'
        form['short_name'] = 'new_short_name'
        form['description'] = 'new_description'
        form['sources'].select_multiple('1')
        resp = form.submit()
        self.assertRedirects(resp, reverse('impacts:list'))
        self.assertEqual(len(Impact.objects.all()), 1)
        impact = Impact.objects.first()
        self.assertEqual(impact.author_id, self.user.username)
        self.assertEqual(impact.name, 'new_name')
        self.assertEqual(impact.short_name, 'new_short_name')
        self.assertEqual(impact.description, 'new_description')


class ImpactsDelete(HSWebTest):
    def setUp(self):
        self.user = UserFactory()
        impact = ImpactFactory(author_id=self.user.username)
        self.url = reverse('impacts:delete', args=(impact.pk, ))

    def test_deletion(self):
        resp = self.app.get(self.url, user=self.user)
        self.form = resp.forms[0]
        resp = self.form.submit()
        self.assertRedirects(resp, reverse('impacts:list'))
        self.assertQuerysetEqual(Impact.objects.all(), [])
