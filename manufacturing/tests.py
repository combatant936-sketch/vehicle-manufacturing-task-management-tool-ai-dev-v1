"""
Tests for Epic 1 — Custom User Model, Auth Views, and Role-Based Access.

Covers:
  - CustomUser model behaviour (M-01 to M-05)
  - CustomUserManager (U-01, U-02)
  - Login / logout / dashboard views (V-01 to V-08)
  - RoleRequiredMixin and @role_required decorator (R-01 to R-05)
"""

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.views import View

from .mixins import ManagerRequiredMixin, role_required

User = get_user_model()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_user(email, role=User.Role.WORKER, password="testpass123", **kwargs):
    return User.objects.create_user(email=email, password=password, role=role, **kwargs)


# ---------------------------------------------------------------------------
# M — CustomUser model
# ---------------------------------------------------------------------------


class CustomUserModelTests(TestCase):
    def test_M01_default_role_is_worker(self):
        """M-01: New user gets the 'worker' role by default."""
        user = User.objects.create_user(email="worker@example.com", password="pass")
        self.assertEqual(user.role, User.Role.WORKER)

    def test_M02_role_properties(self):
        """M-02: is_manager / is_supervisor / is_worker return correct booleans."""
        manager = make_user("mgr@example.com", role=User.Role.MANAGER)
        supervisor = make_user("sup@example.com", role=User.Role.SUPERVISOR)
        worker = make_user("wrk@example.com", role=User.Role.WORKER)

        self.assertTrue(manager.is_manager)
        self.assertFalse(manager.is_supervisor)
        self.assertFalse(manager.is_worker)

        self.assertTrue(supervisor.is_supervisor)
        self.assertFalse(supervisor.is_manager)

        self.assertTrue(worker.is_worker)
        self.assertFalse(worker.is_manager)

    def test_M03_get_full_name_with_names(self):
        """M-03a: get_full_name() returns 'First Last' when both are set."""
        user = make_user("u@example.com", first_name="Jane", last_name="Smith")
        self.assertEqual(user.get_full_name(), "Jane Smith")

    def test_M03_get_full_name_fallback_to_email(self):
        """M-03b: get_full_name() falls back to email when no names are set."""
        user = make_user("u2@example.com")
        self.assertEqual(user.get_full_name(), "u2@example.com")

    def test_M04_str_includes_email_and_role(self):
        """M-04: __str__ contains the email address and role display name."""
        user = make_user("mgr2@example.com", role=User.Role.MANAGER)
        text = str(user)
        self.assertIn("mgr2@example.com", text)
        self.assertIn("Manager", text)

    def test_M05_email_must_be_unique(self):
        """M-05: Saving two users with the same email raises IntegrityError."""
        make_user("dup@example.com")
        with self.assertRaises(IntegrityError):
            make_user("dup@example.com")


# ---------------------------------------------------------------------------
# U — CustomUserManager
# ---------------------------------------------------------------------------


class CustomUserManagerTests(TestCase):
    def test_U01_create_user_without_email_raises(self):
        """U-01: create_user with empty email raises ValueError."""
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="pass")

    def test_U02_create_superuser_sets_flags_and_role(self):
        """U-02: create_superuser sets is_staff, is_superuser, and role=manager."""
        su = User.objects.create_superuser(email="admin@example.com", password="pass")
        self.assertTrue(su.is_staff)
        self.assertTrue(su.is_superuser)
        self.assertEqual(su.role, User.Role.MANAGER)


# ---------------------------------------------------------------------------
# V — Auth views
# ---------------------------------------------------------------------------


class LoginViewTests(TestCase):
    def setUp(self):
        self.url = reverse("login")
        self.user = make_user("login@example.com", password="goodpass")

    def test_V01_get_renders_form(self):
        """V-01: GET /login/ returns 200 with the login form."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manufacturing/login.html")
        self.assertIn("form", response.context)

    def test_V02_authenticated_user_redirected(self):
        """V-02: An already-logged-in user visiting /login/ is redirected to dashboard."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse("dashboard"))

    def test_V03_valid_credentials_log_in_and_redirect(self):
        """V-03: POST with correct email+password logs the user in and redirects to dashboard."""
        response = self.client.post(
            self.url, {"username": "login@example.com", "password": "goodpass"}
        )
        self.assertRedirects(response, reverse("dashboard"))
        # Session should now contain the user id
        self.assertIn("_auth_user_id", self.client.session)

    def test_V04_bad_credentials_return_form_errors(self):
        """V-04: POST with wrong password returns 200 and a non-field error."""
        response = self.client.post(
            self.url, {"username": "login@example.com", "password": "wrongpass"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)

    def test_V05_next_param_redirects_after_login(self):
        """V-05: ?next= is honoured after successful login."""
        target = reverse("dashboard")  # any valid URL
        response = self.client.post(
            f"{self.url}?next={target}",
            {"username": "login@example.com", "password": "goodpass"},
        )
        self.assertRedirects(response, target)


class LogoutViewTests(TestCase):
    def setUp(self):
        self.user = make_user("out@example.com")
        self.client.force_login(self.user)

    def test_V06_logout_clears_session_and_redirects(self):
        """V-06: Visiting /logout/ clears the session and redirects to /login/."""
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("login"))
        self.assertNotIn("_auth_user_id", self.client.session)


class DashboardViewTests(TestCase):
    def setUp(self):
        self.url = reverse("dashboard")
        self.user = make_user("dash@example.com", role=User.Role.SUPERVISOR)

    def test_V07_unauthenticated_redirected_to_login(self):
        """V-07: Unauthenticated GET to / redirects to /login/?next=/."""
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")

    def test_V08_authenticated_user_gets_200_with_role_in_context(self):
        """V-08: Authenticated user gets 200 and can see their role via context user."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["user"].role, User.Role.SUPERVISOR)


# ---------------------------------------------------------------------------
# R — Role-based access control
# ---------------------------------------------------------------------------


class RoleRequiredMixinTests(TestCase):
    """
    Tests for ManagerRequiredMixin (representative of all RoleRequiredMixin subclasses).
    We attach it to a minimal inline view so no URL routing is needed.
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.manager = make_user("mgr@r.com", role=User.Role.MANAGER)
        self.worker = make_user("wrk@r.com", role=User.Role.WORKER)

        # Minimal CBV using the mixin
        class ProtectedView(ManagerRequiredMixin, View):
            def get(self, request, *args, **kwargs):
                from django.http import HttpResponse
                return HttpResponse("ok")

        self.view = ProtectedView.as_view()

    def _request(self, user=None):
        request = self.factory.get("/fake/")
        if user:
            request.user = user
        else:
            from django.contrib.auth.models import AnonymousUser
            request.user = AnonymousUser()
        return request

    def test_R01_unauthenticated_redirected_to_login(self):
        """R-01: Unauthenticated request to a mixin-protected view redirects to login."""
        response = self.view(self._request())
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_R02_correct_role_gets_200(self):
        """R-02: A manager accessing a ManagerRequiredMixin view gets 200."""
        response = self.view(self._request(self.manager))
        self.assertEqual(response.status_code, 200)

    def test_R03_wrong_role_raises_403(self):
        """R-03: A worker accessing a ManagerRequiredMixin view raises PermissionDenied."""
        with self.assertRaises(PermissionDenied):
            self.view(self._request(self.worker))


class RoleRequiredDecoratorTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.manager = make_user("mgr2@r.com", role=User.Role.MANAGER)
        self.supervisor = make_user("sup2@r.com", role=User.Role.SUPERVISOR)

        from django.http import HttpResponse

        @role_required("manager")
        def protected(request):
            return HttpResponse("ok")

        self.protected = protected

    def _request(self, user=None):
        request = self.factory.get("/fake/")
        if user:
            request.user = user
        else:
            from django.contrib.auth.models import AnonymousUser
            request.user = AnonymousUser()
        return request

    def test_R04_unauthenticated_redirected(self):
        """R-04: @role_required redirects unauthenticated users to login."""
        response = self.protected(self._request())
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response["Location"])

    def test_R05_wrong_role_raises_403(self):
        """R-05: @role_required raises PermissionDenied for a user with the wrong role."""
        with self.assertRaises(PermissionDenied):
            self.protected(self._request(self.supervisor))
