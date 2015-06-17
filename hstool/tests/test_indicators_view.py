from django.core.urlresolvers import reverse

from hstool.models import Indicator
from .factories import (
    UserFactory, IndicatorFactory, GeoScopeFactory, EnvironmentalThemeFactory,
)
from . import HSWebTest

REQUIRED = ['This field is required.']
FILETYPE = ['File type not supported: text/x-rst. Please upload only '
            '.pdf, .jpg, .jpeg.']
REQUIRED_COUNTRY = ['The selected Geographical Scale requires a country.']


class IndicatorsList(HSWebTest):
    def setUp(self):
        self.admin = UserFactory(is_superuser=True)
        self.url = reverse('indicators:list')

    def test_one_indicator(self):
        indicator1 = IndicatorFactory()
        resp = self.app.get(self.url, user=self.admin)
        self.assertEqual(resp.pyquery('#objects_listing tbody tr').size(), 1)
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(0) a').text(),
            indicator1.name
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(0) a').attr('href'),
            reverse('indicators:update', args=(indicator1.pk, ))
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(1)').text(),
            indicator1.theme.__unicode__()
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(2)').text(),
            str(indicator1.year_base)
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(3)').text(),
            str(indicator1.year_end)
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(4)').text(),
            indicator1.get_timeline_display()
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(5)').text(),
            str(indicator1.author_id)
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(7) a').attr('href'),
            reverse('indicators:delete', args=(indicator1.pk, ))
        )

    def test_two_indicators(self):
        indicator1 = IndicatorFactory()
        theme = EnvironmentalThemeFactory(title="title2")
        indicator2 = IndicatorFactory(
            author_id='a', name='', short_name='shorty', theme=theme,
            year_base=1111, year_end=2222, timeline=5,
        )
        resp = self.app.get(self.url, user=self.admin)
        self.assertEqual(resp.pyquery('#objects_listing tbody tr').size(), 2)
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(0) a').text(),
            indicator1.name
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(0) a')
            .attr('href'),
            reverse('indicators:update', args=(indicator1.pk, ))
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(1)').text(),
            indicator1.theme.__unicode__()
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(2)').text(),
            str(indicator1.year_base)
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(3)').text(),
            str(indicator1.year_end)
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(4)').text(),
            indicator1.get_timeline_display()
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(5)').text(),
            str(indicator1.author_id)
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(7) a').attr('href'),
            reverse('indicators:delete', args=(indicator1.pk, ))
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(0) a').text(),
            indicator2.name
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(0) a')
            .attr('href'),
            reverse('indicators:update', args=(indicator2.pk, ))
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(1)').text(),
            indicator2.theme.__unicode__()
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(2)').text(),
            str(indicator2.year_base)
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(3)').text(),
            str(indicator2.year_end)
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(4)').text(),
            indicator2.get_timeline_display()
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(5)').text(),
            str(indicator2.author_id)
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(7) a')
            .attr('href'),
            reverse('indicators:delete', args=(indicator2.pk, ))
        )


class IndicatorsAdd(HSWebTest):
    def setUp(self):
        self.user = UserFactory()

    def test_default_fields_required(self):
        url = reverse('indicators:add')
        resp = self.app.get(url, user=self.user)
        form = resp.forms[0]
        resp = form.submit()
        self.assertFormError(resp, 'form', 'theme', REQUIRED)
        self.assertFormError(resp, 'form', 'name', REQUIRED)
        self.assertFormError(resp, 'form', 'short_name', REQUIRED)
        self.assertFormError(resp, 'form', 'year_base', REQUIRED)
        self.assertFormError(resp, 'form', 'year_end', REQUIRED)
        self.assertFormError(resp, 'form', 'timeline', REQUIRED)

    def test_geo_scope_with_country_required(self):
        geo_scope = GeoScopeFactory(title="a", require_country=True)
        url = reverse('indicators:add')
        resp = self.app.get(url, user=self.user)
        form = resp.forms[0]
        form['geographical_scope'].select(text=geo_scope.title)
        resp = form.submit()
        self.assertFormError(resp, 'form', 'country', REQUIRED_COUNTRY)

    def test_successfully_added(self):
        theme = EnvironmentalThemeFactory()
        url = reverse('indicators:add')
        resp = self.app.get(url, user=self.user)
        form = resp.forms[0]
        form['theme'].select(text=theme.title)
        form['name'] = 'a'
        form['short_name'] = 'b'
        form['year_base'] = '1000'
        form['year_end'] = '2000'
        form['timeline'].select(text='daily')
        resp = form.submit()
        self.assertRedirects(resp, reverse('indicators:list'))


class IndicatorsUpdate(HSWebTest):
    def setUp(self):
        self.user = UserFactory()
        self.indicator = IndicatorFactory(author_id=self.user.username)
        self.theme_pk = str(self.indicator.theme.pk)
        url = reverse('indicators:update', args=(self.indicator.pk, ))
        resp = self.app.get(url, user=self.user)
        self.form = resp.forms[0]

    def test_existing_field_values(self):
        self.assertEqual(self.form['theme'].value, self.theme_pk)
        self.assertEqual(self.form['name'].value, self.indicator.name)
        self.assertEqual(self.form['short_name'].value,
                         self.indicator.short_name)
        self.assertEqual(self.form['year_base'].value,
                         str(self.indicator.year_base))
        self.assertEqual(self.form['year_end'].value,
                         str(self.indicator.year_end))
        self.assertEqual(self.form['timeline'].value,
                         str(self.indicator.timeline))

    def test_successfully_updated(self):
        theme = EnvironmentalThemeFactory()
        self.form['theme'].select(text=theme.title)
        self.form['name'] = 'a'
        self.form['short_name'] = 'b'
        self.form['year_base'] = '1111'
        self.form['year_end'] = '2222'
        self.form['timeline'].select(text='monthly')
        resp = self.form.submit()
        self.assertRedirects(resp, reverse('indicators:list'))
        self.assertEqual(len(Indicator.objects.all()), 1)
        indicator = Indicator.objects.first()
        self.assertEqual(indicator.author_id, self.user.username)
        self.assertEqual(indicator.name, 'a')
        self.assertEqual(indicator.short_name, 'b')
        self.assertEqual(indicator.year_base, 1111)
        self.assertEqual(indicator.year_end, 2222)
        self.assertEqual(indicator.timeline, 2)


class IndicatorsDelete(HSWebTest):
    def setUp(self):
        user = UserFactory()
        indicator = IndicatorFactory(author_id=user.username)
        url = reverse('indicators:delete', args=(indicator.pk, ))
        resp = self.app.get(url, user=user)
        self.form = resp.forms[0]

    def test_deletion(self):
        resp = self.form.submit()
        self.assertRedirects(resp, reverse('indicators:list'))
        self.assertQuerysetEqual(Indicator.objects.all(), [])
