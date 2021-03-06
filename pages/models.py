from django.db import models
from django.conf import settings

from translated_fields import TranslatedField, to_attribute
from tinymce import HTMLField
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


class Page(models.Model):
    """A Page Can contain multiple Chunks."""
    slug = models.SlugField(unique=True, help_text=_('str_Page_name'))

    class Meta:
        verbose_name = _('str_page')
        verbose_name_plural = _('str_pages')

    def __unicode__(self):
        return u"%s" % (self.slug,)

    def __str__(self):
        return self.slug


class Chunk(models.Model):
    """
    A Chunk is a piece of content associated
    with a unique key that can be inserted into
    any template with the use of a special template
    tag.
    """
    page = models.ForeignKey(Page, on_delete=models.CASCADE,
                             related_name='chunks')
    key = models.CharField(_('str_Key'),
                           help_text=_("str_Chunk_Key_help_text"),
                           blank=False,
                           max_length=255,
                           unique=True)
    display = models.BooleanField(
            default=True,
            verbose_name=_('str_Display'),
            help_text=_('str_chunk_display_help_text'))
    content = TranslatedField(
                        HTMLField(_('str_Content'), blank=True),
                        {settings.LANGUAGES[0][0]: {"blank": True}},
                        attrgetter=fallback_to_default,)
    description = TranslatedField(
                        models.CharField(_('str_Description'),
                                         blank=True,
                                         max_length=64,
                                         help_text=_("str_Short_description")),
                        {settings.LANGUAGES[0][0]: {"blank": True}},
                        attrgetter=fallback_to_default,)

    objects = ChunkManager()

    class Meta:
        verbose_name = _('str_chunk')
        verbose_name_plural = _('str_chunks')

    def __unicode__(self):
        return u"%s" % (self.key,)

    def __str__(self):
        return self.key
