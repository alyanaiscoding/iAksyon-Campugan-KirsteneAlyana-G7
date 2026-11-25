from django.db import models
from django.conf import settings


class Report(models.Model):

    class Category(models.TextChoices):
        ROAD = "ROAD", "Road Damage"
        GARBAGE = "GARBAGE", "Garbage"
        FLOODING = "FLOODING", "Flooding"
        STREETLIGHT = "STREETLIGHT", "Streetlight"
        OTHER = "OTHER", "Others"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        RESOLVED = "RESOLVED", "Resolved"

    resident = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reports"
    )

    title = models.CharField(max_length=150)

    description = models.TextField()

    category = models.CharField(
        max_length=20,
        choices=Category.choices
    )

    location = models.CharField(max_length=255)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title