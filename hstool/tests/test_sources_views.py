import shutil
import os

from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from webtest import Upload

from .factories import (
    UserFactory, SourceFactory,
)
from . import HSWebTest, MEDIA_ROOT_TEST
from hstool.models import Source

REQUIRED = ['This field is required.']


class SourcesList(HSWebTest):
    def setUp(self):
        self.admin = UserFactory(is_superuser=True)
        self.url = reverse('sources:list')

    def test_one_source(self):
        source1 = SourceFactory()
        resp = self.app.get(self.url, user=self.admin)
        self.assertEqual(resp.pyquery('#objects_listing tbody tr').size(), 1)
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(0) a').text(),
            source1.name
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(0) a').attr('href'),
            reverse('sources:update', args=(source1.pk, ))
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(1)').text(),
            str(source1.published_year)
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(2)').text(),
            source1.author
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(3)').text(),
            source1.author_id
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(6) a').attr('href'),
            reverse('sources:delete', args=(source1.pk, ))
        )

    def test_two_sources(self):
        source1 = SourceFactory()
        source2 = SourceFactory(author_id='a', name='b', title_original='c',
                                published_year=2000, author='d', url='e',
                                file='f', summary='g')
        resp = self.app.get(self.url, user=self.admin)
        self.assertEqual(resp.pyquery('#objects_listing tbody tr').size(), 2)
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(0) a').text(),
            source1.name
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(0) a')
            .attr('href'),
            reverse('sources:update', args=(source1.pk, ))
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(1)').text(),
            str(source1.published_year)
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(2)').text(),
            source1.author
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(3)').text(),
            source1.author_id
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(6) a')
            .attr('href'),
            reverse('sources:delete', args=(source1.pk, ))
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(0) a').text(),
            source2.name
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(0) a')
            .attr('href'),
            reverse('sources:update', args=(source2.pk, ))
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(1)').text(),
            str(source2.published_year)
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(2)').text(),
            source2.author
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(3)').text(),
            source2.author_id
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(6) a')
            .attr('href'),
            reverse('sources:delete', args=(source2.pk, ))
        )


class SourcesAdd(HSWebTest):
    def setUp(self):
        self.user = UserFactory()
        url = reverse('sources:add')
        resp = self.app.get(url, user=self.user)
        self.form = resp.forms[0]

    def test_fields_required(self):
        resp = self.form.submit()
        self.assertFormError(resp, 'form', 'name', REQUIRED)
        self.assertFormError(resp, 'form', 'title_original', REQUIRED)
        self.assertFormError(resp, 'form', 'published_year', REQUIRED)
        self.assertFormError(resp, 'form', 'author', REQUIRED)
        self.assertFormError(resp, 'form', 'file', REQUIRED)
        self.assertFormError(resp, 'form', 'summary', REQUIRED)

    @override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
    def test_successfully_added(self):
        self.form['name'] = 'a'
        self.form['title_original'] = 'b'
        self.form['published_year'] = '2000'
        self.form['author'] = 'd'
        self.form['url'] = 'e'
        self.form['file'] = Upload('b.pdf', b'data', 'application/pdf')
        self.form['summary'] = 'f'
        resp = self.form.submit().follow()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(Source.objects.all()), 1)
        source = Source.objects.first()
        self.assertEqual(source.author_id, self.user.username)
        self.assertEqual(source.name, 'a')
        self.assertEqual(source.title_original, 'b')
        self.assertEqual(source.published_year, 2000)
        self.assertEqual(source.author, 'd')
        self.assertEqual(source.url, 'e')
        self.assertEqual(source.file.name.split('/')[-1], 'b.pdf')
        self.assertEqual(source.summary, 'f')

    def tearDown(self):
        if os.path.isdir(MEDIA_ROOT_TEST):
            shutil.rmtree(MEDIA_ROOT_TEST)


class SourcesUpdate(HSWebTest):
    def setUp(self):
        self.user = UserFactory()
        self.source = SourceFactory(author_id=self.user.username)
        url = reverse('sources:update', args=(self.source.pk, ))
        resp = self.app.get(url, user=self.user)
        self.form = resp.forms[0]

    def test_existing_field_values(self):
        self.assertEqual(self.form['name'].value, self.source.name)
        self.assertEqual(self.form['title_original'].value,
                         self.source.title_original)
        self.assertEqual(self.form['published_year'].value,
                         str(self.source.published_year))
        self.assertEqual(self.form['author'].value, self.source.author)
        self.assertEqual(self.form['url'].value, self.source.url)
        self.assertEqual(self.form['summary'].value, self.source.summary)

    @override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
    def test_successfully_updated(self):
        self.form['name'] = 'a'
        self.form['title_original'] = 'b'
        self.form['published_year'] = '2000'
        self.form['author'] = 'd'
        self.form['url'] = 'e'
        self.form['file'] = Upload('b.pdf', b'data', 'application/pdf')
        self.form['summary'] = 'f'
        resp = self.form.submit().follow()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(Source.objects.all()), 1)
        source = Source.objects.first()
        self.assertEqual(source.author_id, self.user.username)
        self.assertEqual(source.name, 'a')
        self.assertEqual(source.title_original, 'b')
        self.assertEqual(source.published_year, 2000)
        self.assertEqual(source.author, 'd')
        self.assertEqual(source.url, 'e')
        self.assertEqual(source.file.name.split('/')[-1], 'b.pdf')
        self.assertEqual(source.summary, 'f')

    def tearDown(self):
        if os.path.isdir(MEDIA_ROOT_TEST):
            shutil.rmtree(MEDIA_ROOT_TEST)


class SourcesDelete(HSWebTest):
    def setUp(self):
        user = UserFactory()
        source = SourceFactory(author_id=user.username)
        url = reverse('sources:delete', args=(source.pk, ))
        resp = self.app.get(url, user=user)
        self.form = resp.forms[0]

    def test_deletion(self):
        resp = self.form.submit().follow()
        self.assertEqual(resp.status_code, 200)
        self.assertQuerysetEqual(Source.objects.all(), [])
