import shutil
import os

from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from webtest import Upload

from .factories import (
    UserFactory, FigureFactory,
)
from . import HSWebTest, MEDIA_ROOT_TEST
from hstool.models import Figure

REQUIRED = ['This field is required.']
FILETYPE = ['File type not supported: text/x-rst']


class FiguresList(HSWebTest):
    def setUp(self):
        self.admin = UserFactory(is_superuser=True)
        self.url = reverse('figures:list')

    def test_one_figure(self):
        figure1 = FigureFactory(file="b", author_id="c")
        resp = self.app.get(self.url, user=self.admin)
        self.assertEqual(resp.pyquery('#objects_listing tbody tr').size(), 1)
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(0) a').text(),
            figure1.title
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(0) a').attr('href'),
            reverse('figures:update', args=(figure1.pk, ))
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(1) a').text(),
            figure1.file
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(2)').text(),
            figure1.author_id
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(4) a').attr('href'),
            reverse('figures:delete', args=(figure1.pk, ))
        )

    def test_two_figures(self):
        figure1 = FigureFactory(file="b", author_id="c")
        figure2 = FigureFactory(file="bb", author_id="cc")
        resp = self.app.get(self.url, user=self.admin)
        self.assertEqual(resp.pyquery('#objects_listing tbody tr').size(), 2)
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(0) a').text(),
            figure1.title
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(0) a')
            .attr('href'),
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
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(4) a')
            .attr('href'),
            reverse('figures:delete', args=(figure1.pk, ))
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(0) a').text(),
            figure2.title
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(0) a')
            .attr('href'),
            reverse('figures:update', args=(figure2.pk, ))
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(1) a').text(),
            figure2.file,
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(2)').text(),
            figure2.author_id
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(4) a')
            .attr('href'),
            reverse('figures:delete', args=(figure2.pk, ))
        )


class FiguresAdd(HSWebTest):
    def setUp(self):
        user = UserFactory()
        url = reverse('figures:add')
        resp = self.app.get(url, user=user)
        self.form = resp.forms[1]

    def test_fields_required(self):
        resp = self.form.submit()
        self.assertFormError(resp, 'form', 'title', REQUIRED)
        self.assertFormError(resp, 'form', 'file', REQUIRED)

    @override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
    def test_pdf_file(self):
        self.form['title'] = 'a'
        self.form['file'] = Upload('b.pdf', b'data', 'application/pdf')
        resp = self.form.submit().follow()
        self.assertEqual(resp.status_code, 200)

    @override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
    def test_jpg_file(self):
        self.form['title'] = 'a'
        self.form['file'] = Upload('b.jpg', b'data', 'image/jpg')
        resp = self.form.submit().follow()
        self.assertEqual(resp.status_code, 200)

    @override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
    def test_jpeg_file(self):
        self.form['title'] = 'a'
        self.form['file'] = Upload('b.jpeg', b'data', 'image/jpeg')
        resp = self.form.submit().follow()
        self.assertEqual(resp.status_code, 200)

    @override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
    def test_fallback_pdf_file(self):
        self.form['title'] = 'a'
        self.form['file'] = Upload('b.pdf', b'data', 'application/unknown')
        resp = self.form.submit().follow()
        self.assertEqual(resp.status_code, 200)

    def test_unknown_file(self):
        self.form['file'] = Upload('b.rst', b'data', 'text/x-rst')
        resp = self.form.submit()
        self.assertEqual(resp.status_code, 200)
        self.assertFormError(resp, 'form', 'file', FILETYPE)

    @override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
    def test_successfully_added(self):
        self.form['title'] = 'a'
        self.form['file'] = Upload('b.pdf', b'data', 'application/pdf')
        self.form.submit()
        self.assertEqual(len(Figure.objects.all()), 1)
        figure = Figure.objects.first()
        self.assertEqual(figure.title, 'a')
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
        self.form = resp.forms[1]

    def test_existing_field_values(self):
        self.assertEqual(self.form['title'].value, self.figure.title)

    @override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
    def test_pdf_file(self):
        self.form['title'] = 'a'
        self.form['file'] = Upload('b.pdf', b'data', 'application/pdf')
        resp = self.form.submit().follow()
        self.assertEqual(resp.status_code, 200)

    @override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
    def test_jpg_file(self):
        self.form['title'] = 'a'
        self.form['file'] = Upload('b.jpg', b'data', 'image/jpg')
        resp = self.form.submit().follow()
        self.assertEqual(resp.status_code, 200)

    @override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
    def test_jpeg_file(self):
        self.form['title'] = 'a'
        self.form['file'] = Upload('b.jpeg', b'data', 'image/jpeg')
        resp = self.form.submit().follow()
        self.assertEqual(resp.status_code, 200)

    @override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
    def test_fallback_pdf_file(self):
        self.form['title'] = 'a'
        self.form['file'] = Upload('b.pdf', b'data', 'application/unknown')
        resp = self.form.submit().follow()
        self.assertEqual(resp.status_code, 200)

    def test_unknown_file(self):
        self.form['file'] = Upload('b.rst', b'data', 'text/x-rst')
        resp = self.form.submit()
        self.assertEqual(resp.status_code, 200)
        self.assertFormError(resp, 'form', 'file', FILETYPE)

    @override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
    def test_successfully_updated(self):
        self.form['title'] = 'a'
        self.form['file'] = Upload('b.pdf', b'data', 'application/pdf')
        self.form.submit()
        self.assertEqual(len(Figure.objects.all()), 1)
        figure = Figure.objects.first()
        self.assertEqual(figure.title, 'a')
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
        self.form = resp.forms[1]

    def test_deletion(self):
        resp = self.form.submit().follow()
        self.assertEqual(resp.status_code, 200)
        self.assertQuerysetEqual(Figure.objects.all(), [])