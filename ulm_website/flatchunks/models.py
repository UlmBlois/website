from django.db import models


class Flatchunks(models.Model):
    identifier = models.CharField(max_length=20, unique=True, blank=False)
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.identifier)
