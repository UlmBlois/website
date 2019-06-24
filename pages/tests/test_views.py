
from django.test import TestCase

from meeting.tests.utils import ViewTestCase


class PilotInformationsViewTest(ViewTestCase, TestCase):
    url = '/pages/PilotInformations'
    url_name = 'pilot_informations'
    template_name = 'pilot_informations.html'


class AboutViewTest(ViewTestCase, TestCase):
    url = '/pages/About'
    url_name = 'about'
    template_name = 'about.html'


class ContactViewTest(ViewTestCase, TestCase):
    url = '/pages/Contact'
    url_name = 'contact'
    template_name = 'contact.html'


class OnSiteViewTest(ViewTestCase, TestCase):
    url = '/pages/on_site'
    url_name = 'on_site'
    template_name = 'on_site.html'


class PrivacyViewTest(ViewTestCase, TestCase):
    url = '/pages/privacy'
    url_name = 'privacy'
    template_name = 'privacy.html'


class TermsViewTest(ViewTestCase, TestCase):
    url = '/pages/terms'
    url_name = 'terms'
    template_name = 'terms.html'


class CopyrightViewTest(ViewTestCase, TestCase):
    url = '/pages/copyright'
    url_name = 'copyright'
    template_name = 'copyright.html'
