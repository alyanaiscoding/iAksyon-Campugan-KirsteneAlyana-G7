from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.functions import Lower


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        RESIDENT = "RESIDENT", "Resident"
        ADMIN = "ADMIN", "Administrator"

    email = models.EmailField(blank=False)

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.RESIDENT
    )

    contact_number = models.CharField(
        max_length=15,
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("email"),
                name="unique_user_email_ci"
            )
        ]

    def __str__(self):
        return self.username