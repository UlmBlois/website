from django.db import models
from django.conf import settings

from translated_fields import TranslatedField, to_attribute
from django.utils.translation import gettext_lazy as _

from pages.managers import ChunkManager


def fallback_to_default(name):
    def getter(self):
        return getattr(
            self,
            to_attribute(name),
        ) or getattr(
            self,
            # First language acts as fallback:
            to_attribute(name, settings.LANGUAGES[0][0]),
        )
    return getter


class Chunk(models.Model):
    """
    A Chunk is a piece of content associated
    with a unique key that can be inserted into
    any template with the use of a special template
    tag
    """
    key = models.CharField(_('Key'),
                           help_text=_("A unique id for this chunk"),
                           blank=False,
                           max_length=255,
                           unique=True)
    content = TranslatedField(
                        models.TextField(_('Content'), blank=True),
                        {settings.LANGUAGES[0][0]: {"blank": False}},
                        attrgetter=fallback_to_default,)
    description = TranslatedField(
                        models.CharField(_('Description'),
                                         blank=True,
                                         max_length=64,
                                         help_text=_("Short Description")),
                        {settings.LANGUAGES[0][0]: {"blank": False}},
                        attrgetter=fallback_to_default,)

    objects = ChunkManager()

    class Meta:
        verbose_name = _('chunk')
        verbose_name_plural = _('chunks')

    def __unicode__(self):
        return u"%s" % (self.key,)

    def __str__(self):
        return self.key
