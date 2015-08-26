from django.core.urlresolvers import reverse

from hstool.models import SteepCategory, DriverOfChangeType, ImpactType
from .factories import (
    UserFactory, SteepCatFactory, DriverTypeFactory, ImpactTypeFactory
)
from . import HSWebTest

REQUIRED = ['This field is required.']


class SteepCatAdd(HSWebTest):
    def setUp(self):
        self.user = UserFactory(is_superuser=True)
        url = reverse('settings:metadata:steep_category:add')
        self.resp = self.app.get(url, user=self.user)

    def test_default_fields_required(self):
        form = self.resp.forms[0]
        resp = form.submit()
        self.assertFormError(resp, 'form', 'title', REQUIRED)
        self.assertFormError(resp, 'form', 'short_title', REQUIRED)

    def test_successfully_added(self):
        form = self.resp.forms[0]
        form['title'] = 'title'
        form['short_title'] = 'sh'
        resp = form.submit()
        self.assertRedirects(resp, reverse('settings:metadata:steep_category:list'))
        self.assertEqual(len(SteepCategory.objects.all()), 1)


class SteepCatUpdate(HSWebTest):
    def setUp(self):
        self.steep_cat = SteepCatFactory()
        self.user = UserFactory(is_superuser=True)
        self.url = reverse('settings:metadata:steep_category:update',
                           args=(self.steep_cat.pk, ))

    def test_existing_field_values(self):
        resp = self.app.get(self.url, user=self.user)
        form = resp.forms[0]
        self.assertEqual(form['title'].value, self.steep_cat.title)
        self.assertEqual(form['short_title'].value, self.steep_cat.short_title)

    def test_successfully_updated(self):
        resp = self.app.get(self.url, user=self.user)
        form = resp.forms[0]
        form['title'] = 'new_title'
        form['short_title'] = 'nsh'
        resp = form.submit()
        self.assertRedirects(resp, reverse('settings:metadata:steep_category:list'))
        self.assertEqual(len(SteepCategory.objects.all()), 1)
        steep_cat = SteepCategory.objects.first()
        self.assertEqual(steep_cat.title, 'new_title')
        self.assertEqual(steep_cat.short_title, 'nsh')


class SteepCatDelete(HSWebTest):
    def setUp(self):
        steep_cat = SteepCatFactory()
        self.user = UserFactory(is_superuser=True)
        self.url = reverse('settings:metadata:steep_category:delete',
                           args=(steep_cat.pk, ))

    def test_deletion(self):
        resp = self.app.get(self.url, user=self.user)
        self.form = resp.forms[0]
        resp = self.form.submit()
        self.assertRedirects(resp, reverse('settings:metadata:steep_category:list'))
        self.assertQuerysetEqual(SteepCategory.objects.all(), [])


class DriverTypeAdd(HSWebTest):
    def setUp(self):
        self.user = UserFactory(is_superuser=True)
        url = reverse('settings:metadata:doc_type:add')
        self.resp = self.app.get(url, user=self.user)

    def test_default_fields_required(self):
        form = self.resp.forms[0]
        resp = form.submit()
        self.assertFormError(resp, 'form', 'title', REQUIRED)

    def test_successfully_added(self):
        form = self.resp.forms[0]
        form['title'] = 'title'
        resp = form.submit()
        self.assertRedirects(resp, reverse('settings:metadata:doc_type:list'))
        self.assertEqual(len(DriverOfChangeType.objects.all()), 1)


class DriverTypeUpdate(HSWebTest):
    def setUp(self):
        self.doc_type = DriverTypeFactory()
        self.user = UserFactory(is_superuser=True)
        self.url = reverse('settings:metadata:doc_type:update',
                           args=(self.doc_type.pk, ))

    def test_existing_field_values(self):
        resp = self.app.get(self.url, user=self.user)
        form = resp.forms[0]
        self.assertEqual(form['title'].value, self.doc_type.title)

    def test_successfully_updated(self):
        resp = self.app.get(self.url, user=self.user)
        form = resp.forms[0]
        form['title'] = 'new_title'
        resp = form.submit()
        self.assertRedirects(resp, reverse('settings:metadata:doc_type:list'))
        self.assertEqual(len(DriverOfChangeType.objects.all()), 1)
        doc_type = DriverOfChangeType.objects.first()
        self.assertEqual(doc_type.title, 'new_title')


class DriverTypeDelete(HSWebTest):
    def setUp(self):
        doc_type = DriverTypeFactory()
        self.user = UserFactory(is_superuser=True)
        self.url = reverse('settings:metadata:doc_type:delete',
                           args=(doc_type.pk, ))

    def test_deletion(self):
        resp = self.app.get(self.url, user=self.user)
        self.form = resp.forms[0]
        resp = self.form.submit()
        self.assertRedirects(resp, reverse('settings:metadata:doc_type:list'))
        self.assertQuerysetEqual(DriverOfChangeType.objects.all(), [])


class ImpactTypeAdd(HSWebTest):
    def setUp(self):
        self.user = UserFactory(is_superuser=True)
        url = reverse('settings:metadata:impact_type:add')
        self.resp = self.app.get(url, user=self.user)

    def test_default_fields_required(self):
        form = self.resp.forms[0]
        resp = form.submit()
        self.assertFormError(resp, 'form', 'title', REQUIRED)

    def test_successfully_added(self):
        form = self.resp.forms[0]
        form['title'] = 'title'
        resp = form.submit()
        self.assertRedirects(resp, reverse('settings:metadata:impact_type:list'))
        self.assertEqual(len(ImpactType.objects.all()), 1)


class ImpactTypeUpdate(HSWebTest):
    def setUp(self):
        self.impact_type = ImpactTypeFactory()
        self.user = UserFactory(is_superuser=True)
        self.url = reverse('settings:metadata:impact_type:update',
                           args=(self.impact_type.pk, ))

    def test_existing_field_values(self):
        resp = self.app.get(self.url, user=self.user)
        form = resp.forms[0]
        self.assertEqual(form['title'].value, self.impact_type.title)

    def test_successfully_updates(self):
        resp = self.app.get(self.url, user=self.user)
        form = resp.forms[0]
        form['title'] = 'new_title'
        resp = form.submit()
        self.assertRedirects(resp, reverse('settings:metadata:impact_type:list'))
        self.assertEqual(len(ImpactType.objects.all()), 1)
        impact_type = ImpactType.objects.first()
        self.assertEqual(impact_type.title, 'new_title')


class ImpactTypeDelete(HSWebTest):
    def setUp(self):
        impact_type = ImpactTypeFactory()
        self.user = UserFactory(is_superuser=True)
        self.url = reverse('settings:metadata:impact_type:delete',
                           args=(impact_type.pk, ))

    def test_deletion(self):
        resp = self.app.get(self.url, user=self.user)
        self.form = resp.forms[0]
        resp = self.form.submit()
        self.assertRedirects(resp, reverse('settings:metadata:impact_type:list'))
        self.assertQuerysetEqual(ImpactType.objects.all(), [])
