from django.core.urlresolvers import reverse

from hstool.models import Assessment
from .factories import (
    UserFactory, AssessmentFactory, RelationFactory, DriverFactory,
)
from . import HSWebTest

REQUIRED = ['This field is required.']


class AssessmentsList(HSWebTest):
    def setUp(self):
        self.admin = UserFactory(is_superuser=True)
        self.url = reverse('home_view')

    def test_one_assessment(self):
        assessment1 = AssessmentFactory()
        resp = self.app.get(self.url, user=self.admin)
        self.assertEqual(resp.pyquery('#objects_listing tbody tr').size(), 1)
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(0) a').text(),
            assessment1.title
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(0) a').attr('href'),
            reverse('assessments:detail', args=(assessment1.pk, ))
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(1)').text(),
            assessment1.description
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(2)').text(),
            str(assessment1.author_id)
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(5) a').attr('href'),
            reverse('assessments:preview', args=(assessment1.pk, ))
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr td:eq(6) a').attr('href'),
            reverse('assessments:delete', args=(assessment1.pk, ))
        )

    def test_two_assessments(self):
        assessment1 = AssessmentFactory()
        assessment2 = AssessmentFactory(title='title2', description='descr2')
        resp = self.app.get(self.url, user=self.admin)
        self.assertEqual(resp.pyquery('#objects_listing tbody tr').size(), 2)
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(0) a').text(),
            assessment1.title
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(0) a')
            .attr('href'),
            reverse('assessments:detail', args=(assessment1.pk, ))
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(1)').text(),
            assessment1.description
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(2)').text(),
            str(assessment1.author_id)
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(5) a')
            .attr('href'),
            reverse('assessments:preview', args=(assessment1.pk, ))
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(0) td:eq(6) a')
            .attr('href'),
            reverse('assessments:delete', args=(assessment1.pk, ))
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(0) a').text(),
            assessment2.title
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(0) a')
            .attr('href'),
            reverse('assessments:detail', args=(assessment2.pk, ))
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(1)').text(),
            assessment2.description
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(2)').text(),
            str(assessment2.author_id)
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(5) a')
            .attr('href'),
            reverse('assessments:preview', args=(assessment2.pk, ))
        )
        self.assertEqual(
            resp.pyquery('#objects_listing tbody tr:eq(1) td:eq(6) a')
            .attr('href'),
            reverse('assessments:delete', args=(assessment2.pk, ))
        )


class AssessmentsAdd(HSWebTest):
    def setUp(self):
        user = UserFactory()
        url = reverse('assessments:add')
        self.resp = self.app.get(url, user=user)
        self.form = self.resp.forms[0]

    def test_default_fields_required(self):
        resp = self.form.submit()
        self.assertFormError(resp, 'form', 'title', REQUIRED)

    def test_successfully_added(self):
        form = self.resp.forms[0]
        form['title'] = 'a'
        resp = form.submit()
        self.assertRedirects(resp, reverse('assessments:preview', args=(1, )))


class AssessmentsPreview(HSWebTest):
    def setUp(self):
        user = UserFactory()
        self.assessment = AssessmentFactory(author_id=user.username)
        self.driver1 = DriverFactory()
        self.driver2 = DriverFactory(
            author_id='a', name='b', short_name='shorty', type=2, trend_type=2,
            steep_category='T', time_horizon=5,
        )
        self.relation = RelationFactory(
            assessment=self.assessment, source=self.driver1,
            destination=self.driver2
        )
        url = reverse('assessments:preview', args=(self.assessment.pk, ))
        self.resp = self.app.get(url=url, user=user)

    def test_one_relation(self):
        self.assertEqual(self.resp.status_code, 200)
        self.assertTemplateUsed(self.resp, 'tool/assessments_preview.html')
        self.assertEqual(self.resp.pyquery('.page-header').text(),
                         self.assessment.title)
        self.assertEqual(self.resp.pyquery('.assessment-content p').text(),
                         self.assessment.description)
        self.assertEqual(self.resp.pyquery('#objects_listing tbody tr').size(),
                         1)
        self.assertEqual(
            self.resp.pyquery('#objects_listing tbody tr td:eq(0)').text(),
            self.driver1.name
        )
        self.assertEqual(
            self.resp.pyquery('#objects_listing tbody tr td:eq(1)').text(),
            self.relation.get_relationship_type_display()
        )
        self.assertEqual(
            self.resp.pyquery('#objects_listing tbody tr td:eq(2)').text(),
            self.driver2.name
        )
        self.assertEqual(
            self.resp.pyquery('#objects_listing tbody tr td:eq(4) a')
            .attr('href'),
            reverse('relations:update',
                    args=(self.assessment.pk, self.relation.pk, ))
        )
        self.assertEqual(
            self.resp.pyquery('#objects_listing tbody tr td:eq(5) a')
            .attr('href'),
            reverse('relations:delete',
                    args=(self.assessment.pk, self.relation.pk, ))
        )


class AssessmentsUpdate(HSWebTest):
    def setUp(self):
        self.user = UserFactory()
        self.assessment = AssessmentFactory(author_id=self.user.username)
        url = reverse('assessments:update', args=(self.assessment.pk, ))
        resp = self.app.get(url, user=self.user)
        self.form = resp.forms[0]

    def test_existing_field_values(self):
        self.assertEqual(self.form['title'].value, self.assessment.title)
        self.assertEqual(self.form['description'].value,
                         self.assessment.description)

    def test_successfully_updated(self):
        self.form['title'] = 'a'
        self.form['description'] = 'b'
        resp = self.form.submit()
        self.assertRedirects(resp, reverse('assessments:preview',
                                           args=(self.assessment.pk, )))
        self.assertEqual(len(Assessment.objects.all()), 1)
        assessment = Assessment.objects.first()
        self.assertEqual(assessment.author_id, self.user.username)
        self.assertEqual(assessment.title, 'a')
        self.assertEqual(assessment.description, 'b')


class AssessmentsDelete(HSWebTest):
    def setUp(self):
        user = UserFactory()
        assessment = AssessmentFactory(author_id=user.username)
        url = reverse('assessments:delete', args=(assessment.pk, ))
        resp = self.app.get(url, user=user)
        self.form = resp.forms[0]

    def test_deletion(self):
        resp = self.form.submit()
        self.assertRedirects(resp, reverse('home_view'))
        self.assertQuerysetEqual(Assessment.objects.all(), [])
