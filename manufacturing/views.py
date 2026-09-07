from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import LoginForm


def login_view(request):
    """
    Displays the login form and authenticates the user.
    Redirects to the dashboard (or `next` param) on success.
    """
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        next_url = request.GET.get("next") or "dashboard"
        return redirect(next_url)

    return render(request, "manufacturing/login.html", {"form": form})


def logout_view(request):
    """Logs out the current user and redirects to the login page."""
    logout(request)
    return redirect("login")


@login_required
def dashboard_view(request):
    """
    Role-aware landing page.
    Future epics will populate this with real data; for now it simply
    confirms the authenticated role and serves as the post-login target.
    """
    return render(request, "manufacturing/dashboard.html", {"user": request.user})
