from django.contrib import admin
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from translated_fields import TranslatedFieldAdmin, to_attribute
import re
from pages.models import Chunk, Topic, Question


@admin.register(Chunk)
class ChunkAdmin(TranslatedFieldAdmin, admin.ModelAdmin):
    list_display = ('key', "description")

    base_fields = ['description', 'content']
    fieldsets = [
        (_("Globals"), {"fields": ["key"]}),
    ]
    for i, language in enumerate(settings.LANGUAGES):
        ft = []
        for field in base_fields:
            ft.append(
                re.sub(
                    r"[^a-z0-9_]+", "_",
                    ("%s_%s" % (field, language[0])).lower()))
        if i > 0:
            fieldsets.append(
                    (_(language[1]),
                     {"fields": ft, 'classes': ['collapse']}))
        else:
            fieldsets.append((_(language[1]), {"fields": ft}))

    def get_ordering(self, request):
        return [to_attribute("description")]


@admin.register(Topic)
class TopicAdmin(TranslatedFieldAdmin, admin.ModelAdmin):
    list_display = ('topic_name', 'number')

    base_fields = ['topic_name']
    fieldsets = [
        (_("Globals"), {"fields": ["number"]}),
    ]
    for i, language in enumerate(settings.LANGUAGES):
        ft = []
        for field in base_fields:
            ft.append(
                re.sub(
                    r"[^a-z0-9_]+", "_",
                    ("%s_%s" % (field, language[0])).lower()))
        if i > 0:
            fieldsets.append(
                    (_(language[1]),
                     {"fields": ft, 'classes': ['collapse']}))
        else:
            fieldsets.append((_(language[1]), {"fields": ft}))

    def get_ordering(self, request):
        return ['number']


@admin.register(Question)
class QuestionAdmin(TranslatedFieldAdmin, admin.ModelAdmin):
    list_display = ('question', 'topic', 'number')

    base_fields = ['question', 'answer']
    fieldsets = [
        (_("Globals"), {"fields": ["number"]}),
    ]
    for i, language in enumerate(settings.LANGUAGES):
        ft = []
        for field in base_fields:
            ft.append(
                re.sub(
                    r"[^a-z0-9_]+", "_",
                    ("%s_%s" % (field, language[0])).lower()))
        if i > 0:
            fieldsets.append(
                    (_(language[1]),
                     {"fields": ft, 'classes': ['collapse']}))
        else:
            fieldsets.append((_(language[1]), {"fields": ft}))

    def get_ordering(self, request):
        return ['number']
