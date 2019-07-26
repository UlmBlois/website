from django.contrib import admin
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from translated_fields import TranslatedFieldAdmin, to_attribute

from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportMixin

import re
from pages.models import Chunk, Page


def order_fieldset(fieldsets, base_fields):
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


class PageResources(resources.ModelResource):

    class Meta:
        model = Page


@admin.register(Page)
class PageAdmin(ImportExportModelAdmin):
    resource_class = PageResources


class ChunkResources(resources.ModelResource):

    class Meta:
        model = Chunk


@admin.register(Chunk)
class ChunkAdmin(ImportExportMixin, TranslatedFieldAdmin, admin.ModelAdmin):
    list_display = ('key', "description", 'page', 'display')
    list_filter = ['page', 'display']
    base_fields = ['description', 'content']
    resource_class = ChunkResources
    fieldsets = [
        (_("str_Globals"), {"fields": ["key", "page", "display"]}),
    ]
    order_fieldset(fieldsets, base_fields)

    def get_ordering(self, request):
        return [to_attribute("description")]
