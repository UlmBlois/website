from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


class SimpleFile(models.Model):
    key = models.CharField(max_length=20, unique=True, blank=False)
    file = models.FileField()

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        super(SimpleFile, self).save(*args, **kwargs)
        # filename = self.data.url


@receiver(post_delete, sender=SimpleFile)
def submission_delete(sender, instance, **kwargs):
    instance.file.delete(False)
