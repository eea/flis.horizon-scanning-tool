from django.core.urlresolvers import reverse

from hstool.models import SteepCategory, DriverOfChangeType
from .factories import (
    UserFactory, SteepCatFactory, DriverTypeFactory
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


class DriverTypeUpdayr(HSWebTest):
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
