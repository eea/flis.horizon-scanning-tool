from django.core.urlresolvers import reverse

from .factories import (
    UserFactory, AssessmentFactory, DriverFactory, FigureFactory,
    SourceFactory, GeoScopeFactory, CountryFactory,
    EnvironmentalThemeFactory, RelationFactory,
)
from . import HSWebTest


class AssessmentsListViewTests(HSWebTest):
    def test_list_anonymous(self):
        url = reverse('home_view')
        resp = self.app.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_list_authenticated(self):
        url = reverse('home_view')
        user = UserFactory()
        resp = self.app.get(url, user=user)
        self.assertEqual(resp.status_code, 200)


class AssessmentsAddViewTests(HSWebTest):
    def test_add_anonymous(self):
        url = reverse('assessments:add')
        resp = self.app.get(url, expect_errors=True)
        self.assertEqual(resp.status_code, 403)

    def test_add_authenticated(self):
        url = reverse('assessments:add')
        user = UserFactory()
        resp = self.app.get(url, user=user)
        self.assertEqual(resp.status_code, 200)


class AssessmentsDetailTests(HSWebTest):
    def setUp(self):
        self.user = UserFactory()
        self.assessment = AssessmentFactory(author_id=self.user.username)
        self.url = reverse('assessments:detail', args=(self.assessment.pk, ))

    def test_anonymous(self):
        resp = self.app.get(self.url, expect_errors=True)
        self.assertEqual(resp.status_code, 403)

    def test_authenticated_other(self):
        user2 = UserFactory(username="username2")
        resp = self.app.get(self.url, expect_errors=True, user=user2)
        self.assertEqual(resp.status_code, 403)

    def test_authenticated_author(self):
        resp = self.app.get(self.url, user=self.user)
        self.assertEqual(resp.status_code, 200)

    def test_admin(self):
        admin = UserFactory(username='admin', is_superuser=True)
        resp = self.app.get(self.url, user=admin)
        self.assertEqual(resp.status_code, 200)


class AssessmentsUpdateViewTests(HSWebTest):
    def setUp(self):
        self.user = UserFactory()
        self.assessment = AssessmentFactory(author_id=self.user.username)
        self.url = reverse('assessments:update', args=(self.assessment.pk, ))

    def test_update_anonymous(self):
        resp = self.app.get(self.url, expect_errors=True)
        self.assertEqual(resp.status_code, 403)

    def test_update_authenticated_author(self):
        resp = self.app.get(self.url, user=self.user)
        self.assertEqual(resp.status_code, 200)

    def test_update_authenticated_other(self):
        user2 = UserFactory(username="username2")
        resp = self.app.get(self.url, expect_errors=True, user=user2)
        self.assertEqual(resp.status_code, 403)

    def test_update_admin(self):
        admin = UserFactory(username='admin', is_superuser=True)
        resp = self.app.get(self.url, user=admin)
        self.assertEqual(resp.status_code, 200)


class AssessmentsDeleteViewTests(HSWebTest):
    def setUp(self):
        self.user = UserFactory()
        self.assessment = AssessmentFactory(author_id=self.user.username)
        self.url = reverse('assessments:delete', args=(self.assessment.pk, ))

    def test_delete_anonymous(self):
        resp = self.app.get(self.url, expect_errors=True)
        self.assertEqual(resp.status_code, 403)

    def test_delete_authenticated_author(self):
        resp = self.app.get(self.url, user=self.user)
        self.assertEqual(resp.status_code, 200)

    def test_delete_authenticated_other(self):
        user2 = UserFactory(username="username2")
        resp = self.app.get(self.url, expect_errors=True, user=user2)
        self.assertEqual(resp.status_code, 403)

    def test_delete_admin(self):
        admin = UserFactory(username='admin', is_superuser=True)
        resp = self.app.get(self.url, user=admin)
        self.assertEqual(resp.status_code, 200)


class RelationsAddViewTests(HSWebTest):
    def setUp(self):
        self.user = UserFactory()
        assessment = AssessmentFactory(author_id=self.user.username)
        self.url = reverse('relations:add', args=(assessment.pk, ))

    def test_add_anonymous(self):
        resp = self.app.get(self.url, expect_errors=True)
        self.assertEqual(resp.status_code, 403)

    def test_add_authenticated_other(self):
        user2 = UserFactory(username="username2")
        resp = self.app.get(self.url, expect_errors=True, user=user2)
        self.assertEqual(resp.status_code, 403)

    def test_add_authenticated_owner(self):
        resp = self.app.get(self.url, user=self.user)
        self.assertEqual(resp.status_code, 200)

    def test_add_admin(self):
        admin = UserFactory(username='admin', is_superuser=True)
        resp = self.app.get(self.url, user=admin)
        self.assertEqual(resp.status_code, 200)


class RelationsUpdateViewTests(HSWebTest):
    def setUp(self):
        self.user = UserFactory()
        assessment = AssessmentFactory(author_id=self.user.username)
        figureindicator = FigureFactory()
        driver = DriverFactory()
        relation = RelationFactory(
            assessment=assessment, source=driver, destination=figureindicator
        )
        self.url = reverse('relations:update',
                           args=(assessment.pk, relation.pk))

    def test_update_anonymous(self):
        resp = self.app.get(self.url, expect_errors=True)
        self.assertEqual(resp.status_code, 403)

    def test_update_authenticated_author(self):
        resp = self.app.get(self.url, user=self.user)
        self.assertEqual(resp.status_code, 200)

    def test_update_authenticated_other(self):
        user2 = UserFactory(username="username2")
        resp = self.app.get(self.url, expect_errors=True, user=user2)
        self.assertEqual(resp.status_code, 403)

    def test_update_admin(self):
        admin = UserFactory(username='admin', is_superuser=True)
        resp = self.app.get(self.url, user=admin)
        self.assertEqual(resp.status_code, 200)


class RelationsDeleteViewTests(HSWebTest):
    def setUp(self):
        self.user = UserFactory()
        assessment = AssessmentFactory(author_id=self.user.username)
        figureindicator = FigureFactory()
        driver = DriverFactory()
        relation = RelationFactory(
            assessment=assessment, source=driver, destination=figureindicator
        )
        self.url = reverse('relations:delete',
                           args=(assessment.pk, relation.pk))

    def test_delete_anonymous(self):
        resp = self.app.get(self.url, expect_errors=True)
        self.assertEqual(resp.status_code, 403)

    def test_delete_authenticated_author(self):
        resp = self.app.get(self.url, user=self.user)
        self.assertEqual(resp.status_code, 200)

    def test_delete_authenticated_other(self):
        user2 = UserFactory(username="username2")
        resp = self.app.get(self.url, expect_errors=True, user=user2)
        self.assertEqual(resp.status_code, 403)

    def test_delete_admin(self):
        admin = UserFactory(username='admin', is_superuser=True)
        resp = self.app.get(self.url, user=admin)
        self.assertEqual(resp.status_code, 200)


class DriversListViewTests(HSWebTest):
    def test_list_anonymous(self):
        url = reverse('drivers:list')
        resp = self.app.get(url, expect_errors=True)
        self.assertEqual(resp.status_code, 403)

    def test_list_authenticated(self):
        url = reverse('drivers:list')
        user = UserFactory()
        resp = self.app.get(url, user=user)
        self.assertEqual(resp.status_code, 200)


class DriversAddViewTests(HSWebTest):
    def test_add_anonymous(self):
        url = reverse('drivers:add')
        resp = self.app.get(url, expect_errors=True)
        self.assertEqual(resp.status_code, 403)

    def test_add_authenticated(self):
        url = reverse('drivers:add')
        user = UserFactory()
        resp = self.app.get(url, user=user)
        self.assertEqual(resp.status_code, 200)


class DriversUpdateViewTests(HSWebTest):
    def setUp(self):
        self.user = UserFactory()
        self.driver = DriverFactory(author_id=self.user.username)
        self.url = reverse('drivers:update', args=(self.driver.pk, ))

    def test_update_anonymous(self):
        resp = self.app.get(self.url, expect_errors=True)
        self.assertEqual(resp.status_code, 403)

    def test_update_authenticated_author(self):
        resp = self.app.get(self.url, user=self.user)
        self.assertEqual(resp.status_code, 200)

    def test_update_authenticated_other(self):
        user2 = UserFactory(username="username2")
        resp = self.app.get(self.url, expect_errors=True, user=user2)
        self.assertEqual(resp.status_code, 403)

    def test_update_admin(self):
        admin = UserFactory(username='admin', is_superuser=True)
        resp = self.app.get(self.url, user=admin)
        self.assertEqual(resp.status_code, 200)


class DriversDeleteViewTests(HSWebTest):
    def setUp(self):
        self.user = UserFactory()
        self.driver = DriverFactory(author_id=self.user.username)
        self.url = reverse('drivers:delete', args=(self.driver.pk, ))

    def test_delete_anonymous(self):
        resp = self.app.get(self.url, expect_errors=True)
        self.assertEqual(resp.status_code, 403)

    def test_delete_authenticated_author(self):
        resp = self.app.get(self.url, user=self.user)
        self.assertEqual(resp.status_code, 200)

    def test_delete_authenticated_other(self):
        user2 = UserFactory(username="username2")
        resp = self.app.get(self.url, expect_errors=True, user=user2)
        self.assertEqual(resp.status_code, 403)

    def test_delete_admin(self):
        admin = UserFactory(username='admin', is_superuser=True)
        resp = self.app.get(self.url, user=admin)
        self.assertEqual(resp.status_code, 200)

class SourcesListViewTests(HSWebTest):
    def test_list_anonymous(self):
        url = reverse('sources:list')
        resp = self.app.get(url, expect_errors=True)
        self.assertEqual(resp.status_code, 403)

    def test_list_authenticated(self):
        url = reverse('sources:list')
        user = UserFactory()
        resp = self.app.get(url, user=user)
        self.assertEqual(resp.status_code, 200)


class SourcesAddViewTests(HSWebTest):
    def test_add_anonymous(self):
        url = reverse('sources:add')
        resp = self.app.get(url, expect_errors=True)
        self.assertEqual(resp.status_code, 403)

    def test_add_authenticated(self):
        url = reverse('sources:add')
        user = UserFactory()
        resp = self.app.get(url, user=user)
        self.assertEqual(resp.status_code, 200)


class SourcesUpdateViewTests(HSWebTest):
    def setUp(self):
        self.user = UserFactory()
        self.source = SourceFactory(author_id=self.user.username)
        self.url = reverse('sources:update', args=(self.source.pk, ))

    def test_update_anonymous(self):
        resp = self.app.get(self.url, expect_errors=True)
        self.assertEqual(resp.status_code, 403)

    def test_update_authenticated_author(self):
        resp = self.app.get(self.url, user=self.user)
        self.assertEqual(resp.status_code, 200)

    def test_update_authenticated_other(self):
        user2 = UserFactory(username="username2")
        resp = self.app.get(self.url, expect_errors=True, user=user2)
        self.assertEqual(resp.status_code, 403)

    def test_update_admin(self):
        admin = UserFactory(username='admin', is_superuser=True)
        resp = self.app.get(self.url, user=admin)
        self.assertEqual(resp.status_code, 200)


class SourcesDeleteViewTests(HSWebTest):
    def setUp(self):
        self.user = UserFactory()
        self.source = SourceFactory(author_id=self.user.username)
        self.url = reverse('sources:delete', args=(self.source.pk, ))

    def test_delete_anonymous(self):
        resp = self.app.get(self.url, expect_errors=True)
        self.assertEqual(resp.status_code, 403)

    def test_delete_authenticated_author(self):
        resp = self.app.get(self.url, user=self.user)
        self.assertEqual(resp.status_code, 200)

    def test_delete_authenticated_other(self):
        user2 = UserFactory(username="username2")
        resp = self.app.get(self.url, expect_errors=True, user=user2)
        self.assertEqual(resp.status_code, 403)

    def test_delete_admin(self):
        admin = UserFactory(username='admin', is_superuser=True)
        resp = self.app.get(self.url, user=admin)
        self.assertEqual(resp.status_code, 200)


class FiguresListViewTests(HSWebTest):
    def test_list_anonymous(self):
        url = reverse('figures:list')
        resp = self.app.get(url, expect_errors=True)
        self.assertEqual(resp.status_code, 403)

    def test_list_authenticated(self):
        url = reverse('figures:list')
        user = UserFactory()
        resp = self.app.get(url, user=user)
        self.assertEqual(resp.status_code, 200)


class FiguresAddViewTests(HSWebTest):
    def test_add_anonymous(self):
        url = reverse('figures:add')
        resp = self.app.get(url, expect_errors=True)
        self.assertEqual(resp.status_code, 403)

    def test_add_authenticated(self):
        url = reverse('figures:add')
        user = UserFactory()
        resp = self.app.get(url, user=user)
        self.assertEqual(resp.status_code, 200)


class FiguresUpdateViewTests(HSWebTest):
    def setUp(self):
        self.user = UserFactory()
        self.figure = FigureFactory(author_id=self.user.username)
        self.url = reverse('figures:update', args=(self.figure.pk, ))

    def test_update_anonymous(self):
        resp = self.app.get(self.url, expect_errors=True)
        self.assertEqual(resp.status_code, 403)

    def test_update_authenticated_author(self):
        resp = self.app.get(self.url, user=self.user)
        self.assertEqual(resp.status_code, 200)

    def test_update_authenticated_other(self):
        user2 = UserFactory(username="username2")
        resp = self.app.get(self.url, expect_errors=True, user=user2)
        self.assertEqual(resp.status_code, 403)

    def test_update_admin(self):
        admin = UserFactory(username='admin', is_superuser=True)
        resp = self.app.get(self.url, user=admin)
        self.assertEqual(resp.status_code, 200)


class FiguresDeleteViewTests(HSWebTest):
    def setUp(self):
        self.user = UserFactory()
        self.figure = FigureFactory(author_id=self.user.username)
        self.url = reverse('figures:delete', args=(self.figure.pk, ))

    def test_delete_anonymous(self):
        resp = self.app.get(self.url, expect_errors=True)
        self.assertEqual(resp.status_code, 403)

    def test_delete_authenticated_author(self):
        resp = self.app.get(self.url, user=self.user)
        self.assertEqual(resp.status_code, 200)

    def test_delete_authenticated_other(self):
        user2 = UserFactory(username="username2")
        resp = self.app.get(self.url, expect_errors=True, user=user2)
        self.assertEqual(resp.status_code, 403)

    def test_delete_admin(self):
        admin = UserFactory(username='admin', is_superuser=True)
        resp = self.app.get(self.url, user=admin)
        self.assertEqual(resp.status_code, 200)


class RolesOverviewTests(HSWebTest):
    def setUp(self):
        self.url = reverse('settings:roles')

    def test_list_anonymous(self):
        resp = self.app.get(self.url, expect_errors=True)
        self.assertEqual(resp.status_code, 403)

    def test_list_authenticated_not_admin(self):
        user = UserFactory()
        resp = self.app.get(self.url, expect_errors=True, user=user)
        self.assertEqual(resp.status_code, 403)

    def test_list_authenticated_as_admin(self):
        admin = UserFactory(is_superuser=True)
        resp = self.app.get(self.url, user=admin)
        self.assertEqual(resp.status_code, 200)
