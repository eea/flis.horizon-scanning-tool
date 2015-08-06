from django.core.urlresolvers import reverse
from .factories import (
    UserFactory, IndicatorFactory, ImpactFactory
)
from . import HSWebTest

REQUIRED = ['This field is required.']


class UserEntriesList(HSWebTest):
    def setUp(self):
        self.admin = UserFactory(is_superuser=True)
        self.url = reverse('entries:list')

    def test_one_entry(self):
        indicator = IndicatorFactory()
        resp = self.app.get(self.url, user=self.admin)
        self.assertEqual(resp.pyquery('#objects_listing tbody tr').size(), 1)
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(1)').text(),
            indicator.name
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(1) a').attr('href'),
            reverse('indicators:update', args=(indicator.pk, ))
        )

        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(3) a').attr('href'),
            reverse('entries:delete', args=(indicator.pk, ))
        )

    def test_two_entries(self):
        indicator = IndicatorFactory()
        impact = ImpactFactory()
        resp = self.app.get(self.url, user=self.admin)
        self.assertEqual(resp.pyquery('#objects_listing tbody tr').size(), 2)
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(1)').text(),
            indicator.name
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(1) a').attr('href'),
            reverse('indicators:update', args=(indicator.pk, ))
        )

        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(3) a').attr('href'),
            reverse('entries:delete', args=(indicator.pk, ))
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(1)').text(),
            impact.name
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(1) a').attr('href'),
            reverse('impacts:update', args=(impact.pk, ))
        )

        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(3) a').attr('href'),
            reverse('entries:delete', args=(impact.pk, ))
        )