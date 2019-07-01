# Python
from datetime import date, timedelta
import logging

# Django
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator
# Third party
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
# Owned
from meeting.managers import (MeetingManager, TimeSlotManager,
                              ReservationManager)
from radio_call_sign_field.modelfields import RadioCallSignField

logger = logging.getLogger(__name__)


###############################################################################
#       MEETING
###############################################################################

class Meeting(models.Model):
    """Model reprenseting an edition of the meating."""
    name = models.CharField(max_length=128)
    registration_start = models.DateField()
    registration_end = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    confirmation_reminder_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=False)
    fuel_aviable = models.PositiveIntegerField(default=0)

    objects = MeetingManager()

    def __str__(self):
        """String representing the Meeting object."""
        return str(self.name)

    def save(self, *args, **kwargs):
        if self.confirmation_reminder_date is None:
            self.confirmation_reminder_date = self.start_date - timedelta(7)

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
        return self.registration_start <= date.today() <= self.registration_end

    def registration_open_at(self, date):
        return self.registration_start <= date <= self.registration_end

    @property
    def registration_aviable(self):
        aviables = TimeSlot.objects.aviables()
        return self.registration_open and len(aviables) > 1

    @property
    def confirmation_open(self):
        return (self.confirmation_reminder_date <= date.today()
                <= self.start_date)


###############################################################################
#       TIMESLOTS
###############################################################################

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
            timezone.localtime(self.start_date).strftime("%A %I:%M"),
            timezone.localtime(self.end_date).strftime("%I:%M"))

    def clean(self, *args, **kwargs):
        # TODO: a completer
        if self.start_date >= self.end_date:
            raise ValidationError(_('str_Error_Timeslot_Start_Superior_End'))
        if (self.start_date.date() < self.meeting.start_date
                or self.meeting.end_date < self.start_date.date()):
            raise ValidationError(_('str_Error_Timeslot_Start_Out_Of_Meeting'))
        if (self.end_date.date() < self.meeting.start_date
                or self.meeting.end_date < self.end_date.date()):
            raise ValidationError(_('str_Error_Timeslot_End_Out_Of_Meeting'))
        super(TimeSlot, self).clean(*args, **kwargs)


###############################################################################
#       PILOT
###############################################################################

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Pilot.objects.create(user=instance)
    instance.pilot.save()


class Pilot(models.Model):
    """Model reprenseting a pilot."""
    AELIA = "AELIA"
    AEPAL = "AEPAL"
    AIG = "AIG"
    AIR_COURTAGE = "AIR COURTAGE"
    AISCAIR = "AISCAIR"
    AISCALE = "AISCALE"
    ALBION = "ALBION"
    ALKORA = "ALKORA"
    ALLIANZ = "ALLIANZ"
    ALPHA = "ALPHA INSURANCE"
    AMTI = "AMTI"
    ASSUAERO = "ASSUAERO"
    AXA = "AXA"
    BENACQUISTA = "BENACQUISTA"
    BHPA = "BHPA"
    CATLIN = "CATLIN INSURANCE"

    INSURANCE_CHOICES = (
        (AELIA, AELIA),
        (AEPAL, AEPAL),
        (AIG, AIG),
        (AIR_COURTAGE, AIR_COURTAGE),
        (AISCAIR, AISCAIR),
        (AISCALE, AISCALE),
        (ALBION, ALBION),
        (ALKORA, ALKORA),
        (ALLIANZ, ALLIANZ),
        (ALPHA, ALPHA),
        (AMTI, AMTI),
        (ASSUAERO, ASSUAERO),
        (AXA, AXA),
        (BENACQUISTA, BENACQUISTA),
        (BHPA, BHPA),
        (CATLIN, CATLIN),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    insurance_company = models.CharField(max_length=64)
    insurance_number = models.CharField(max_length=64)
    licence_number = models.CharField(max_length=64)
    phone_number = PhoneNumberField(help_text=_('str_helptext_phonenumber'),
                                    null=True)  # TODO: remove null=True in production
    modification_date = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = (
            (
             'reservation_validation',
             _('str_Reservation_Validation_Permission')
            ),
        )

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

    @property
    def as_unconfirmed_reservation(self):
        meeting = Meeting.objects.active()
        return Reservation.objects.filter(
                pilot=self, meeting=meeting, confirmed=False).exists()

    @property
    def as_active_reservation(self):
        meeting = Meeting.objects.active()
        return Reservation.objects.filter(pilot=self, meeting=meeting).exists()

    @property
    def can_make_reservation(self):
        return not self.as_active_reservation

###############################################################################
#       ULM
###############################################################################


class ULM(models.Model):
    """Model reprenseting an ULM."""
    # PARAMOTOR = 'PA'
    PENDULAR = 'PE'
    MULTIAXES = 'MU'
    AUTOGYRE = 'AU'
    HELICOPETER = 'HE'
    AEROSTAT = 'AE'
    ULM_TYPE_CHOICE = [
        # (PARAMOTOR, _("str_Powered_Paraglider")),
        (PENDULAR, _("str_Flex_Wing")),
        (MULTIAXES, _("str_Fixed_Wings")),
        (AUTOGYRE, _("str_Rotor_Wings")),
        (HELICOPETER, _("str_Helicopters")),
        (AEROSTAT, _("str_Balloons_and_Airships"))
    ]

    pilot = models.ForeignKey(Pilot, on_delete=models.CASCADE,
                              related_name='ulm')
    constructor = models.CharField(max_length=32)
    model = models.CharField(max_length=32)
    type = models.CharField(
        max_length=2,
        choices=ULM_TYPE_CHOICE,
    )
    imatriculation_country = CountryField()
    imatriculation = models.CharField(max_length=6)
    radio_id = RadioCallSignField()

    def __str__(self):
        return str(self.radio_id)

    def display_pilot(self):
        return f'{self.pilot}'

    def get_type_display(self):
        return dict(self.ULM_TYPE_CHOICE).get(self.type, '')

    display_pilot.short_description = 'Pilot'


###############################################################################
#       RESERVATION
###############################################################################


class Reservation(models.Model):
    """Model reprenseting a reservation for an in flight arrival."""
    ulm = models.ForeignKey(ULM, on_delete=models.SET_NULL, null=True,
                            related_name="reservations")
    pilot = models.ForeignKey(Pilot, on_delete=models.SET_NULL, null=True)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    reservation_number = models.CharField(max_length=32, unique=True)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE,
                                  related_name='arrivals', null=True)
    depart_time_slot = models.ForeignKey(TimeSlot, on_delete=models.SET_NULL,
                                         related_name='departures', null=True)
    arrival = models.DateTimeField(null=True, default=None, blank=True)
    fuel_reservation = models.PositiveIntegerField(
            default=0,
            validators=[MaxValueValidator(100)])
    fuel_served = models.PositiveIntegerField(default=0)
    flight_plan = models.BooleanField(default=False)
    passanger = models.BooleanField(default=False)
    esthetic_cup = models.BooleanField(default=False)
    for_sale = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)
    fuel_reservation_confirmed = models.BooleanField(default=False)
    fuel_advance = models.PositiveIntegerField(default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    origin_city = models.CharField(max_length=64, blank=True)  # TODO move into profile
    origin_field = models.CharField(max_length=4, blank=True,
                                    help_text=_("str_Airfield_OACI_code"))  # TODO move into profile

    objects = ReservationManager()

    def validate_unique(self, exclude):
        super().validate_unique(exclude)
        # self.meeting and self.pilot are not initialized at this stage
        if self._state.adding:
            ts_valid = (self.time_slot and Reservation.objects.filter(
                pilot=self.ulm.pilot,
                meeting=self.time_slot.meeting).exists())
            if ts_valid:
                raise ValidationError(
                    _('str_Error_Reservation_Allready_Exist'))

    def is_active(self):
        return self.meeting.active

    def __str__(self):
        """String reprenseting a reservation."""
        return f'{self.reservation_number}'

    def display_pilot(self):
        if self.ulm is not None:
            return f'{self.pilot}'
        else:
            return '-'

    def is_missing_informations(self):
        # TODO: a completer
        if self.ulm is None or self.pilot is None:
            return False
        if self.pilot.licence_number == "":
            return True
        if self.pilot.insurance_number == "":
            return True
        if self.pilot.insurance_company == "":
            return True
        return False

    def is_confirmed(self):
        return not self.canceled and self.confirmed

    def is_on_time(self):
        """Check if the pilot is arrived during his timeslot"""
        if self.arrival_delay().seconds/3600 < 4:
            return True
        else:
            return False

    def arrival_delay(self):
        if self.arrival is not None:
            if timezone.is_naive(self.arrival):
                arrival = timezone.make_aware(self.arrival)
            else:
                arrival = self.arrival
        else:
            arrival = timezone.now()
        delta1 = arrival - timezone.localtime(self.time_slot.start_date)
        delta2 = arrival - timezone.localtime(self.time_slot.end_date)
        delay = min(delta1, delta2)
        return delay

    display_pilot.short_description = _('str_Pilot')


##############################################################################
# RECEIVER
##############################################################################

@receiver(pre_save, sender=ULM)
def normalize_ULM(sender, instance, **kwargs):
    instance.radio_id = instance.radio_id.upper()
    instance.imatriculation = instance.imatriculation.upper()


@receiver(pre_save, sender=Reservation)
def init_shortcut_fields(sender, instance, **kwargs):
    if not instance.pilot and instance.ulm:
        instance.pilot = instance.ulm.pilot
    if not instance.meeting and instance.time_slot:
        instance.meeting = instance.time_slot.meeting
