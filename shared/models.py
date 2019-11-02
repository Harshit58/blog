from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and Time when the object was created.")
    modified = models.DateTimeField(
        auto_now=True,
        help_text="Date and Time when the object was last modified.")

    class Meta:
        abstract = True
