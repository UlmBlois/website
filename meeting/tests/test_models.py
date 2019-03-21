from django.test import TestCase
import datetime
from meeting.models import Meeting


class MeetingTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Meeting.objects.create(name="1",
                               registration_start=datetime.date(2019, 3, 15),
                               registration_end=datetime.date(2019, 4, 15),
                               start_date=datetime.date(2019, 8, 30),
                               end_date=datetime.date(2019, 9, 1),
                               active=True, fuel_aviable=100)
        Meeting.objects.create(name="2",
                               registration_start=datetime.date(2018, 3, 15),
                               registration_end=datetime.date(2018, 4, 15),
                               start_date=datetime.date(2018, 8, 30),
                               end_date=datetime.date(2018, 9, 1),
                               active=False, fuel_aviable=100)

    def test_registration_open_at(self):  # same test as registration_open
        meeting = Meeting.objects.get(name="1")
        self.assertTrue(meeting.registration_open_at(
            datetime.date(2019, 3, 15)))
        self.assertFalse(meeting.registration_open_at(
            datetime.date(2019, 3, 1)))
        self.assertFalse(meeting.registration_open_at(
            datetime.date(2019, 5, 1)))

    def test_save(self):
        meeting2 = Meeting.objects.get(name="2")
        meeting2.active = True
        meeting2.save()
        self.assertTrue(Meeting.objects.get(name="2").active)
        self.assertFalse(Meeting.objects.get(name="1").active)
        Meeting.objects.get(name="1").update(active=True)
