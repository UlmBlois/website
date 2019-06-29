from django.contrib import admin
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from translated_fields import TranslatedFieldAdmin, to_attribute
import re
from pages.models import Chunk, Page
import logging

logger = logging.getLogger(__name__)


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


@admin.register(Chunk)
class ChunkAdmin(TranslatedFieldAdmin, admin.ModelAdmin):
    list_display = ('key', "description", 'page')
    list_filter = ['page']
    base_fields = ['description', 'content']
    fieldsets = [
        (_("str_Globals"), {"fields": ["key", "page"]}),
    ]
    for i, language in enumerate(settings.LANGUAGES):
        ft = []
        for field in base_fields:
            ft.append(
                re.sub(
                    r"[^a-z0-9_]+", "_",
                    ("%s_%s" % (field, language[0])).lower()))
        if settings.LANGUAGE_CODE == language[0]:
            fieldsets.insert(1, (_(language[1]), {"fields": ft}))
        else:
            fieldsets.append((
                            _(language[1]),
                            {"fields": ft, 'classes': ['collapse']}
                            ))

    def get_ordering(self, request):
        return [to_attribute("description")]
