from django.db import models
from django.conf import settings

from translated_fields import TranslatedField, to_attribute
from tinymce import HTMLField
from django.utils.translation import gettext_lazy as _


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


class Topic(models.Model):
    """FAQ Topics."""
    topic_name = TranslatedField(
                        models.CharField(
                                max_length=200,
                                verbose_name=_("topic")),
                        {settings.LANGUAGES[0][0]: {"blank": False}},
                        attrgetter=fallback_to_default,)
    number = models.PositiveIntegerField(unique=True)

    class Meta:
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")
        ordering = ['number']

    def __unicode__(self):
        return u'(%s) %s' % (self.number, self.topic_name, )

    def __str__(self):
        return self.topic_name


class Question(models.Model):
    """FAQ Questions."""
    question = TranslatedField(
                            models.CharField(
                                max_length=200,
                                verbose_name=_("question")),
                            {settings.LANGUAGES[0][0]: {"blank": False}},
                            attrgetter=fallback_to_default,)
    answer = TranslatedField(
                            HTMLField(
                                verbose_name=_("answer")),
                            {settings.LANGUAGES[0][0]: {"blank": False}},
                            attrgetter=fallback_to_default,)
    topic = models.ForeignKey(Topic, related_name='question',
                              on_delete=models.CASCADE)
    number = models.PositiveIntegerField()

    class Meta:
        unique_together = ("number", "topic")
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ['number']

    def __unicode__(self):
        return u'(%s) %s' % (self.number, self.question, )

    def __str__(self):
        return self.question
