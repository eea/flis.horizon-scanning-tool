import shutil
import os

from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from webtest import Upload

from .factories import (
    UserFactory, FigureFactory, EnvironmentalThemeFactory
)
from . import HSWebTest, MEDIA_ROOT_TEST
from hstool.models import FigureIndicator

REQUIRED = ['This field is required.']
FILETYPE = ['File type not supported: text/x-rst']


class FiguresList(HSWebTest):
    def setUp(self):
        self.admin = UserFactory(is_superuser=True)
        self.url = reverse('figures:list')

    def test_one_figure(self):
        figure = FigureFactory()
        resp = self.app.get(self.url, user=self.admin)
        self.assertEqual(resp.pyquery('#objects_listing tbody tr').size(), 1)
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(0) a').text(),
            figure.name
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(0) a').attr('href'),
            reverse('figures:update', args=(figure.pk, ))
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(1) a').text(),
            figure.file
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(2)').text(),
            figure.author_id
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(4)').text(),
            figure.theme.__unicode__()
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(5)').text(),
            figure.url
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(8)').text(),
            figure.is_indicator
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(9) a').attr('href'),
            reverse('figures:delete', args=(figure.pk, ))
        )

    def test_two_figures(self):
        figure1 = FigureFactory()
        theme = EnvironmentalThemeFactory(title='title')
        figure2 = FigureFactory(author_id='a2', name='title2', theme=theme,
                                is_indicator='yes', file='file2', url='url2')
        resp = self.app.get(self.url, user=self.admin)
        self.assertEqual(resp.pyquery('#objects_listing tbody tr').size(), 2)
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(0) a').text(),
            figure1.name
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(0) a').attr('href'),
            reverse('figures:update', args=(figure1.pk, ))
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(1) a').text(),
            figure1.file
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(2)').text(),
            figure1.author_id
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(4)').text(),
            figure1.theme.__unicode__()
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(5)').text(),
            figure1.url
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(8)').text(),
            figure1.is_indicator
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(9) a').attr('href'),
            reverse('figures:delete', args=(figure1.pk, ))
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(0) a').text(),
            figure2.name
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(0) a').attr('href'),
            reverse('figures:update', args=(figure2.pk, ))
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(1) a').text(),
            figure2.file
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(2)').text(),
            figure2.author_id
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(4)').text(),
            figure2.theme.__unicode__()
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(5)').text(),
            figure2.url
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(8)').text(),
            figure2.is_indicator
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(9) a').attr('href'),
            reverse('figures:delete', args=(figure2.pk, ))
        )


class FiguresAdd(HSWebTest):
    def setUp(self):
        user = UserFactory()
        EnvironmentalThemeFactory()
        url = reverse('figures:add')
        resp = self.app.get(url, user=user)
        self.form = resp.forms[0]


    def test_fields_required(self):
        resp = self.form.submit()
        self.assertFormError(resp, 'form', 'name', REQUIRED)
        self.assertFormError(resp, 'form', 'file', REQUIRED)
        self.assertFormError(resp, 'form', 'theme', REQUIRED)

    @override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
    def test_pdf_file(self):
        self.form['name'] = 'a'
        self.form['file'] = Upload('b.pdf', b'data', 'application/pdf')
        theme = EnvironmentalThemeFactory()
        self.form['theme'].select(text=theme.title)
        resp = self.form.submit().follow()
        self.assertEqual(resp.status_code, 200)

    @override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
    def test_jpg_file(self):
        self.form['name'] = 'a'
        self.form['file'] = Upload('b.jpg', b'data', 'image/jpg')
        theme = EnvironmentalThemeFactory()
        self.form['theme'].select(text=theme.title)
        resp = self.form.submit().follow()

        self.assertEqual(resp.status_code, 200)

    @override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
    def test_jpeg_file(self):
        self.form['name'] = 'a'
        self.form['file'] = Upload('b.jpeg', b'data', 'image/jpeg')
        theme = EnvironmentalThemeFactory()
        self.form['theme'].select(text=theme.title)
        resp = self.form.submit().follow()
        self.assertEqual(resp.status_code, 200)

    @override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
    def test_fallback_pdf_file(self):
        self.form['name'] = 'a'
        self.form['file'] = Upload('b.pdf', b'data', 'application/unknown')
        theme = EnvironmentalThemeFactory()
        self.form['theme'].select(text=theme.title)
        resp = self.form.submit().follow()
        self.assertEqual(resp.status_code, 200)

    def test_unknown_file(self):
        self.form['name'] = 'a'
        self.form['file'] = Upload('b.rst', b'data', 'text/x-rst')
        theme = EnvironmentalThemeFactory(title='title')
        self.form['theme'].select(text=theme.title)
        resp = self.form.submit()
        self.assertEqual(resp.status_code, 200)
        self.assertFormError(resp, 'form', 'file', FILETYPE)

    @override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
    def test_successfully_added(self):
        url = reverse('figures:add')
        resp = self.app.get(url)
        form = resp.forms[0]
        self.form['name'] = 'a'
        self.form['file'] = Upload('b.pdf', b'data', 'application/pdf')
        theme = EnvironmentalThemeFactory(title='title')
        self.form['theme'].select(text=theme.title)
        self.form.submit()
        self.assertEqual(len(FigureIndicator.objects.all()), 1)
        figure = FigureIndicator.objects.first()
        self.assertEqual(figure.name, 'a')
        self.assertEqual(figure.file.name.split('/')[-1], 'b.pdf')

    def tearDown(self):
        if os.path.isdir(MEDIA_ROOT_TEST):
            shutil.rmtree(MEDIA_ROOT_TEST)


class FiguresUpdate(HSWebTest):
    def setUp(self):
        user = UserFactory()
        self.figure = FigureFactory(author_id=user.username)
        url = reverse('figures:update', args=(self.figure.pk, ))
        resp = self.app.get(url, user=user)
        self.form = resp.forms[0]

    def test_existing_field_values(self):
        self.assertEqual(self.form['name'].value, self.figure.name)

    @override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
    def test_pdf_file(self):
        self.form['name'] = 'a'
        self.form['file'] = Upload('b.pdf', b'data', 'application/pdf')
        theme = EnvironmentalThemeFactory()
        self.form['theme'].select(text=theme.title)
        resp = self.form.submit().follow()
        self.assertEqual(resp.status_code, 200)

    @override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
    def test_jpg_file(self):
        self.form['name'] = 'a'
        self.form['file'] = Upload('b.jpg', b'data', 'image/jpg')
        theme = EnvironmentalThemeFactory()
        self.form['theme'].select(text=theme.title)
        resp = self.form.submit().follow()
        self.assertEqual(resp.status_code, 200)

    @override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
    def test_jpeg_file(self):
        self.form['name'] = 'a'
        self.form['file'] = Upload('b.jpeg', b'data', 'image/jpeg')
        theme = EnvironmentalThemeFactory()
        self.form['theme'].select(text=theme.title)
        resp = self.form.submit().follow()
        self.assertEqual(resp.status_code, 200)

    @override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
    def test_fallback_pdf_file(self):
        self.form['name'] = 'a'
        self.form['file'] = Upload('b.pdf', b'data', 'application/unknown')
        theme = EnvironmentalThemeFactory()
        self.form['theme'].select(text=theme.title)
        resp = self.form.submit().follow()
        self.assertEqual(resp.status_code, 200)

    def test_unknown_file(self):
        self.form['file'] = Upload('b.rst', b'data', 'text/x-rst')
        self.form['name'] = 'a'
        theme = EnvironmentalThemeFactory()
        self.form['theme'].select(text=theme.title)
        resp = self.form.submit()
        self.assertEqual(resp.status_code, 200)
        self.assertFormError(resp, 'form', 'file', FILETYPE)

    @override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
    def test_successfully_updated(self):
        self.form['name'] = 'a'
        theme = EnvironmentalThemeFactory()
        self.form['theme'].select(text=theme.title)
        self.form['file'] = Upload('b.pdf', b'data', 'application/pdf')
        self.form.submit()
        self.assertEqual(len(FigureIndicator.objects.all()), 1)
        figure = FigureIndicator.objects.first()
        self.assertEqual(figure.name, 'a')
        self.assertEqual(figure.file.name.split('/')[-1], 'b.pdf')

    def tearDown(self):
        if os.path.isdir(MEDIA_ROOT_TEST):
            shutil.rmtree(MEDIA_ROOT_TEST)


class FiguresDelete(HSWebTest):
    def setUp(self):
        user = UserFactory()
        figure = FigureFactory(author_id=user.username)
        url = reverse('figures:delete', args=(figure.pk, ))
        resp = self.app.get(url, user=user)
        self.form = resp.forms[0]

    def test_deletion(self):
        resp = self.form.submit().follow()
        self.assertEqual(resp.status_code, 200)
        self.assertQuerysetEqual(FigureIndicator.objects.all(), [])
