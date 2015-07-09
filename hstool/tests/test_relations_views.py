from django.core.urlresolvers import reverse

from hstool.models import Relation
from .factories import (
    UserFactory, RelationFactory, AssessmentFactory, DriverFactory,
    FigureFactory, EnvironmentalThemeFactory,
)
from . import HSWebTest

REQUIRED = ['This field is required.']


class RelationsAdd(HSWebTest):
    def setUp(self):
        user = UserFactory()
        self.driver = DriverFactory()
        self.figureindicator = FigureFactory()
        self.assessment = AssessmentFactory(author_id=user.username)
        url = reverse('relations:add', args=(self.assessment.pk, ))
        self.resp = self.app.get(url, user=user)

    def test_default_fields_required(self):
        form = self.resp.forms[0]
        resp = form.submit()
        self.assertFormError(resp, 'form', 'source', REQUIRED)
        self.assertFormError(resp, 'form', 'destination', REQUIRED)
        self.assertFormError(resp, 'form', 'figureindicators', [])

    def test_successfully_added(self):
        form = self.resp.forms[0]
        form['source'].select(text=self.driver.name)
        form['relationship_type'].select(text='Neutral relationship')
        form['description'] = 'description'
        form['figureindicator'] = '2'
        resp = form.submit()
        self.assertRedirects(resp, reverse('assessments:detail',
                                           args=(self.assessment.pk, )))
        self.assertEqual(len(Relation.objects.all()), 1)


class RelationsUpdate(HSWebTest):
    def setUp(self):
        self.user = UserFactory()
        driver1 = DriverFactory()
        indicator1 = FigureFactory()
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
        self.assertEqual(form['relationship_type'].value,
                         str(self.relation.relationship_type))
        self.assertEqual(form['description'].value,
                         self.relation.description)

    def test_successfully_updated(self):
        theme = EnvironmentalThemeFactory()
        driver2 = DriverFactory(
            author_id='a', name='longy d', short_name='shorty d', type=2,
            trend_type=2, steep_category='T', time_horizon=5,
        )
        indicator2 = FigureFactory(
            author_id='a', name='title1', theme=theme, is_indicator=True, file="file1", url='url1'
        )
        resp = self.app.get(self.url, user=self.user)
        form = resp.forms[0]
        form['source'].select(text=driver2.name)
        form['figureindicator'] = '4'
        resp = form.submit()
        self.assertRedirects(resp, reverse('assessments:detail',
                                           args=(self.assessment.pk, )))
        self.assertEqual(len(Relation.objects.all()), 1)
        relation = Relation.objects.first()
        self.assertEqual(relation.source.pk, driver2.pk)
        self.assertEqual(relation.destination.pk, indicator2.pk)


class RelationsDelete(HSWebTest):
    def setUp(self):
        user = UserFactory()
        driver1 = DriverFactory()
        indicator1 = FigureFactory()
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
        self.assertRedirects(resp, reverse('assessments:detail',
                                           args=(self.assessment.pk, )))
        self.assertQuerysetEqual(Relation.objects.all(), [])
