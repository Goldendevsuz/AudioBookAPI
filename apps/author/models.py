from django.db import models
from django_extensions.db.models import TimeStampedModel


class Author(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
