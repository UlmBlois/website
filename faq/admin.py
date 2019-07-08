from django.contrib import admin
from django.conf import settings

import re

from django.utils.translation import gettext_lazy as _

from import_export import resources
from import_export.admin import ImportExportMixin
from translated_fields import TranslatedFieldAdmin

from faq.models import Topic, Question


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


class TopicResources(resources.ModelResource):

    class Meta:
        model = Topic


@admin.register(Topic)
class TopicAdmin(ImportExportMixin, TranslatedFieldAdmin, admin.ModelAdmin):
    list_display = ('topic_name', 'number')
    base_fields = ['topic_name']
    resource_class = TopicResources
    fieldsets = [
        (_("str_Globals"), {"fields": ["number"]}),
    ]
    order_fieldset(fieldsets, base_fields)

    def get_ordering(self, request):
        return ['number']


class QuestionResources(resources.ModelResource):

    class Meta:
        model = Question


@admin.register(Question)
class QuestionAdmin(ImportExportMixin, TranslatedFieldAdmin, admin.ModelAdmin):
    list_display = ('question', 'topic', 'number')
    list_filter = ['topic']
    base_fields = ['question', 'answer']
    resource_class = QuestionResources
    fieldsets = [
        (_("str_Globals"), {"fields": ["number", "topic"]}),
    ]
    order_fieldset(fieldsets, base_fields)

    def get_ordering(self, request):
        return ['number']
