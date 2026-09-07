from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for the Vehicle Manufacturing Task Management System.

    Uses email as the primary identifier and adds a role field to distinguish
    between the three system actors: manager, supervisor, and worker.
    """

    class Role(models.TextChoices):
        MANAGER = "manager", "Manager"
        SUPERVISOR = "supervisor", "Supervisor"
        WORKER = "worker", "Worker"

    email = models.EmailField(unique=True, verbose_name="Email address")
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.WORKER,
        db_index=True,
    )

    # Standard Django permission/admin flags
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # email + password are enough for createsuperuser

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["email"]

    def __str__(self):
        return f"{self.get_full_name()} <{self.email}> [{self.get_role_display()}]"

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.email

    def get_short_name(self):
        return self.first_name or self.email

    # ------------------------------------------------------------------
    # Convenience role-check properties
    # ------------------------------------------------------------------

    @property
    def is_manager(self):
        return self.role == self.Role.MANAGER

    @property
    def is_supervisor(self):
        return self.role == self.Role.SUPERVISOR

    @property
    def is_worker(self):
        return self.role == self.Role.WORKER
