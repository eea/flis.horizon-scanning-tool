from django.core.urlresolvers import reverse

from hstool.models import DriverOfChange
from .factories import (
    UserFactory, DriverFactory, GeoScopeFactory,
)
from . import HSWebTest

REQUIRED = ['This field is required.']
FILETYPE = ['File type not supported: text/x-rst. Please upload only '
            '.pdf, .jpg, .jpeg.']
REQUIRED_COUNTRY = ['The selected Geographical Scale requires a country.']


class DriversList(HSWebTest):
    def setUp(self):
        self.admin = UserFactory(is_superuser=True)
        self.url = reverse('drivers:list')

    def test_one_driver(self):
        driver1 = DriverFactory()
        resp = self.app.get(self.url, user=self.admin)
        self.assertEqual(resp.pyquery('#objects_listing tbody tr').size(), 1)
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(0) a').text(),
            driver1.name
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(0) a').attr('href'),
            reverse('drivers:update', args=(driver1.pk, ))
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(1)').text(),
            driver1.get_type_display()
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(2)').text(),
            driver1.get_trend_type_display()
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(4)').text(),
            driver1.get_steep_category_display()
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(5)').text(),
            driver1.get_time_horizon_display()
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(6)').text(),
            str(driver1.author_id)
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(7) a').attr('href'),
            reverse('drivers:delete', args=(driver1.pk, ))
        )

    def test_two_drivers(self):
        driver1 = DriverFactory()
        driver2 = DriverFactory(
            author_id='a', name='', short_name='shorty', type=2, trend_type=2,
            steep_category='T', time_horizon=5,
        )
        resp = self.app.get(self.url, user=self.admin)
        self.assertEqual(resp.pyquery('#objects_listing tbody tr').size(), 2)
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(0) a').text(),
            driver1.name
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(0) a')
            .attr('href'),
            reverse('drivers:update', args=(driver1.pk, ))
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(1)').text(),
            driver1.get_type_display()
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(2)').text(),
            driver1.get_trend_type_display()
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(4)').text(),
            driver1.get_steep_category_display()
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(5)').text(),
            driver1.get_time_horizon_display()
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(6)').text(),
            str(driver1.author_id)
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(7) a').attr('href'),
            reverse('drivers:delete', args=(driver1.pk, ))
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(0) a').text(),
            driver2.name
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(0) a')
            .attr('href'),
            reverse('drivers:update', args=(driver2.pk, ))
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(1)').text(),
            driver2.get_type_display()
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(4)').text(),
            driver2.get_steep_category_display()
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(5)').text(),
            driver2.get_time_horizon_display()
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(6)').text(),
            str(driver2.author_id)
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(7) a')
            .attr('href'),
            reverse('drivers:delete', args=(driver2.pk, ))
        )


class DriversAdd(HSWebTest):
    def setUp(self):
        self.user = UserFactory()

    def test_default_fields_required(self):
        url = reverse('drivers:add')
        resp = self.app.get(url, user=self.user)
        form = resp.forms[0]
        resp = form.submit()
        self.assertFormError(resp, 'form', 'name', REQUIRED)
        self.assertFormError(resp, 'form', 'short_name', REQUIRED)
        self.assertFormError(resp, 'form', 'type', REQUIRED)
        self.assertFormError(resp, 'form', 'steep_category', REQUIRED)
        self.assertFormError(resp, 'form', 'time_horizon', REQUIRED)

    def test_geo_scope_with_country_required(self):
        geo_scope = GeoScopeFactory(title="a", require_country=True)
        url = reverse('drivers:add')
        resp = self.app.get(url, user=self.user)
        form = resp.forms[0]
        form['geographical_scope'].select(text=geo_scope.title)
        resp = form.submit()
        self.assertFormError(resp, 'form', 'country', REQUIRED_COUNTRY)

    def test_successfully_added(self):
        url = reverse('drivers:add')
        resp = self.app.get(url, user=self.user)
        form = resp.forms[0]
        form['name'] = 'a'
        form['short_name'] = 'b'
        form['type'].select(text='Trends')
        form['trend_type'].select(text='Trend')
        form['steep_category'].select(text='Political')
        form['time_horizon'].select(text='1 year')
        resp = form.submit()
        self.assertRedirects(resp, reverse('drivers:list'))


class DriversUpdate(HSWebTest):
    def setUp(self):
        self.user = UserFactory()
        self.driver = DriverFactory(author_id=self.user.username)
        url = reverse('drivers:update', args=(self.driver.pk, ))
        resp = self.app.get(url, user=self.user)
        self.form = resp.forms[0]

    def test_existing_field_values(self):
        self.assertEqual(self.form['name'].value, self.driver.name)
        self.assertEqual(self.form['short_name'].value, self.driver.short_name)
        self.assertEqual(self.form['type'].value, str(self.driver.type))
        self.assertEqual(self.form['trend_type'].value,
                         str(self.driver.trend_type))
        self.assertEqual(self.form['steep_category'].value,
                         str(self.driver.steep_category))
        self.assertEqual(self.form['time_horizon'].value,
                         str(self.driver.time_horizon))

    def test_successfully_updated(self):
        self.form['name'] = 'a'
        self.form['short_name'] = 'b'
        self.form['type'].select(text='Uncertainties')
        self.form['trend_type'].select(text='Megatrend')
        self.form['steep_category'].select(text='Social')
        self.form['time_horizon'].select(text='5 years')
        resp = self.form.submit()
        self.assertRedirects(resp, reverse('drivers:list'))
        self.assertEqual(len(DriverOfChange.objects.all()), 1)
        driver = DriverOfChange.objects.first()
        self.assertEqual(driver.author_id, self.user.username)
        self.assertEqual(driver.name, 'a')
        self.assertEqual(driver.short_name, 'b')
        self.assertEqual(driver.type, 2)
        self.assertEqual(driver.trend_type, 2)
        self.assertEqual(driver.steep_category, 'S')
        self.assertEqual(driver.time_horizon, 5)


class DriversDelete(HSWebTest):
    def setUp(self):
        user = UserFactory()
        driver = DriverFactory(author_id=user.username)
        url = reverse('drivers:delete', args=(driver.pk, ))
        resp = self.app.get(url, user=user)
        self.form = resp.forms[0]

    def test_deletion(self):
        resp = self.form.submit()
        self.assertRedirects(resp, reverse('drivers:list'))
        self.assertQuerysetEqual(DriverOfChange.objects.all(), [])
