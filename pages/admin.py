from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from translated_fields import TranslatedFieldAdmin, to_attribute
from pages.models import Chunk


@admin.register(Chunk)
class ChunkAdmin(TranslatedFieldAdmin, admin.ModelAdmin):
    list_display = ('key', "description")

    # Pack question and answer fields into their own fieldsets:
    fieldsets = [
        (_("description"), {"fields": Chunk.description.fields}),
        (_("content"), {"fields": Chunk.content.fields}),
    ]

    def get_ordering(self, request):
        return [to_attribute("description")]
