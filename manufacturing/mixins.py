"""
Role-based access control mixins and decorators.

Usage examples
--------------

Class-based views:

    class MyView(ManagerRequiredMixin, View):
        ...

    class MyView(RoleRequiredMixin, View):
        required_roles = ['manager', 'supervisor']
        ...

Function-based views:

    @role_required('manager')
    def my_view(request):
        ...

    @role_required('manager', 'supervisor')
    def my_view(request):
        ...
"""

from functools import wraps

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class RoleRequiredMixin(LoginRequiredMixin):
    """
    Mixin that restricts access to users whose role is in `required_roles`.

    Subclasses must define:
        required_roles = ['manager']          # list of allowed roles
    """

    required_roles: list[str] = []

    def dispatch(self, request, *args, **kwargs):
        # LoginRequiredMixin handles unauthenticated users first
        response = super().dispatch(request, *args, **kwargs)
        if not request.user.is_authenticated:
            return response
        if self.required_roles and request.user.role not in self.required_roles:
            raise PermissionDenied
        return response


class ManagerRequiredMixin(RoleRequiredMixin):
    """Restricts access to users with the 'manager' role."""

    required_roles = ["manager"]


class SupervisorRequiredMixin(RoleRequiredMixin):
    """Restricts access to users with the 'supervisor' role."""

    required_roles = ["supervisor"]


class WorkerRequiredMixin(RoleRequiredMixin):
    """Restricts access to users with the 'worker' role."""

    required_roles = ["worker"]


class ManagerOrSupervisorRequiredMixin(RoleRequiredMixin):
    """Restricts access to managers and supervisors."""

    required_roles = ["manager", "supervisor"]


# ---------------------------------------------------------------------------
# Function-based view decorators
# ---------------------------------------------------------------------------


def role_required(*roles):
    """
    Decorator for function-based views.

    @role_required('manager')
    @role_required('manager', 'supervisor')
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                from django.conf import settings
                from django.shortcuts import redirect

                return redirect(f"{settings.LOGIN_URL}?next={request.path}")
            if request.user.role not in roles:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
