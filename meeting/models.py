from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
from datetime import date

from meeting.managers import MeetingManager, TimeSlotManager


class Meeting(models.Model):
    """Model reprenseting an edition of the meating."""
    name = models.CharField(
        max_length=128,
        help_text='Enter the meeting name (e.g Salon Ulm 2018)')
    registration_start = models.DateField()
    registration_end = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField(default=False)
    fuel_aviable = models.PositiveIntegerField(default=0)

    objects = MeetingManager()

    def __str__(self):
        """String representing the Meeting object."""
        return str(self.name)

    def save(self, *args, **kwargs):
        if self.active:
            # select all other active items
            qs = type(self).objects.filter(active=True)
            # except self (if self already exists)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            # and deactive them
            qs.update(active=False)

        super(Meeting, self).save(*args, **kwargs)

    @property
    def registration_open(self):
        return (date.today() >= self.registration_start
                and self.registration_end > date.today())

    def registration_open_at(self, date):
        return (date >= self.registration_start
                and self.registration_end > date)


class TimeSlot(models.Model):
    """Model representing an arrival time slot."""
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    arrivals_slots = models.PositiveIntegerField()

    objects = TimeSlotManager()

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        """String representing an arrivals time slot."""
        return "{}-{}".format(
            self.start_date.strftime("%A %I:%M"),
            self.end_date.strftime("%I:%M"))


class Pilot(models.Model):
    """Model reprenseting a pilot."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    insurance_number = models.CharField(max_length=64)
    licence_number = models.CharField(max_length=64)
    licence_file = models.FileField(null=True, blank=True)
    insurance_file = models.FileField(null=True, blank=True)
    last_update = models.DateField(null=True, blank=True)  # insurance_file

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Pilot.objects.create(user=instance)
    instance.pilot.save()


class ULM(models.Model):
    """Model reprenseting an ULM."""
    pilot = models.ForeignKey(Pilot, on_delete=models.CASCADE)
    constructor = models.CharField(max_length=32)
    model = models.CharField(max_length=32)
    imatriculation_country = CountryField(default='FR')
    imatriculation = models.CharField(max_length=16)
    radio_id = models.CharField(max_length=16)

    def __str__(self):
        return str(self.radio_id)

    def display_pilot(self):
        return f'{self.ulm.pilot}'

    display_pilot.short_description = 'Pilot'


class Reservation(models.Model):
    """Model reprenseting a reservation for an in flight arrival."""
    ulm = models.ForeignKey(ULM, on_delete=models.CASCADE)
    reservation_number = models.CharField(max_length=32, unique=True)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    arrival = models.DateTimeField(null=True, default=None)
    fuel_reservation = models.PositiveIntegerField(default=0)
    fuel_served = models.BooleanField(default=False)
    flight_plan = models.BooleanField(default=False)
    passanger = models.BooleanField(default=False)
    esthetic_cup = models.BooleanField(default=False)
    to_sell = models.BooleanField(default=False)

    def validate_unique(self, exclude):
        super().validate_unique(exclude)
        if self._state.adding:
            if Reservation.objects.filter(
                ulm__pilot=self.ulm.pilot,
                    time_slot__meeting=self.time_slot.meeting).count() > 0:
                raise ValidationError(
                    'You allready have a reservation for this meeting, please edit or delete the existing one'
                    )

    def is_active(self):
        return self.time_slot.meeting.active

    def __str__(self):
        """String reprenseting a reservation."""
        return f'{self.reservation_number}'

    def display_pilot(self):
        return f'{self.ulm.pilot}'

    display_pilot.short_description = 'Pilot'
