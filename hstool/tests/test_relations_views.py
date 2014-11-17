from django.core.urlresolvers import reverse

from hstool.models import Relation
from .factories import (
    UserFactory, RelationFactory, AssessmentFactory, DriverFactory,
    IndicatorFactory, EnvironmentalThemeFactory,
)
from . import HSWebTest

REQUIRED = ['This field is required.']


class RelationsAdd(HSWebTest):
    def setUp(self):
        user = UserFactory()
        self.driver = DriverFactory()
        self.indicator = IndicatorFactory()
        self.assessment = AssessmentFactory(author_id=user.username)
        url = reverse('relations:add', args=(self.assessment.pk, ))
        self.resp = self.app.get(url, user=user)

    def test_default_fields_required(self):
        form = self.resp.forms[0]
        resp = form.submit()
        self.assertFormError(resp, 'form', 'source', REQUIRED)
        self.assertFormError(resp, 'form', 'destination', REQUIRED)
        self.assertFormError(resp, 'form', 'relationship_type', REQUIRED)
        self.assertFormError(resp, 'form', 'description', REQUIRED)
        self.assertFormError(resp, 'form', 'figures', [])

    def test_successfully_added(self):
        form = self.resp.forms[0]
        form['source'].select(text=self.driver.name)
        form['destination'].select(text=self.indicator.name)
        form['relationship_type'].select(text='Neutral relationship')
        form['description'] = 'description'
        resp = form.submit()
        self.assertRedirects(resp, reverse('assessments:preview',
                                           args=(self.assessment.pk, )))
        self.assertEqual(len(Relation.objects.all()), 1)


class RelationsUpdate(HSWebTest):
    def setUp(self):
        self.user = UserFactory()
        driver1 = DriverFactory()
        indicator1 = IndicatorFactory()
        self.assessment = AssessmentFactory(author_id=self.user.username)
        self.relation = RelationFactory(
            assessment=self.assessment, source=driver1, destination=indicator1
        )
        self.url = reverse('relations:update', args=(self.assessment.pk,
                                                     self.relation.pk, ))

    def test_existing_field_values(self):
        resp = self.app.get(self.url, user=self.user)
        form = resp.forms[0]
        self.assertEqual(form['source'].value, str(self.relation.source.pk))
        self.assertEqual(form['destination'].value,
                         str(self.relation.destination.pk))
        self.assertEqual(form['relationship_type'].value,
                         str(self.relation.relationship_type))
        self.assertEqual(form['description'].value,
                         self.relation.description)

    def test_successfully_updated(self):
        theme = EnvironmentalThemeFactory(title='title 2')
        driver2 = DriverFactory(
            author_id='a', name='longy d', short_name='shorty d', type=2,
            trend_type=2, steep_category='T', time_horizon=5,
        )
        indicator2 = IndicatorFactory(
            author_id='a', name='longy i', short_name='shorty i', theme=theme,
            year_base=1111, year_end=2222, timeline=5,
        )
        resp = self.app.get(self.url, user=self.user)
        form = resp.forms[0]
        form['source'].select(text=driver2.name)
        form['destination'].select(text=indicator2.name)
        form['relationship_type'].select(text='Neutral relationship')
        form['description'] = 'description 2'
        resp = form.submit()
        self.assertRedirects(resp, reverse('assessments:preview',
                                           args=(self.assessment.pk, )))
        self.assertEqual(len(Relation.objects.all()), 1)
        relation = Relation.objects.first()
        self.assertEqual(relation.source.pk, driver2.pk)
        self.assertEqual(relation.destination.pk, indicator2.pk)
        self.assertEqual(relation.relationship_type, 2)
        self.assertEqual(relation.description, 'description 2')


class RelationsDelete(HSWebTest):
    def setUp(self):
        user = UserFactory()
        driver1 = DriverFactory()
        indicator1 = IndicatorFactory()
        self.assessment = AssessmentFactory(author_id=user.username)
        relation = RelationFactory(
            assessment=self.assessment, source=driver1, destination=indicator1
        )
        url = reverse('relations:delete', args=(self.assessment.pk,
                                                relation.pk, ))
        resp = self.app.get(url, user=user)
        self.form = resp.forms[0]

    def test_deletion(self):
        resp = self.form.submit()
        self.assertRedirects(resp, reverse('assessments:preview',
                                           args=(self.assessment.pk, )))
        self.assertQuerysetEqual(Relation.objects.all(), [])
