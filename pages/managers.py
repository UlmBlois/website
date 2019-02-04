from django.db import models
from pages import models as mod

class ChunkManager(models.Manager):

    def safe_get(self, **kwargs):
        try:
            go = mod.Chunk.objects.get(**kwargs)
        except mod.Chunk.DoesNotExist:
            go = None
        return go
