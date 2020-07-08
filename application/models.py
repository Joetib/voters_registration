from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from .utils import verify_from_nia

# Create your models here.

User = get_user_model()


class UserProfile(models.Model):
    # The user the profile belongs to
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    # the user's profile picture
    picture = models.ImageField(upload_to="images/", blank=True, null=True)
    # Specifies whether the user's details have been verified. That is
    # whether the national_id_no entered is correct.
    verified = models.BooleanField(default=False)
    # The user's national id card number
    national_id_no = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if (not self.verified) and self.national_id_no:
            self.verify()
        super().save(*args, **kwargs)

    def verify(self, *args, **kwargs):
        if self.verified:
            return True
        elif self.national_id_no:
            if verify_from_nia(self.national_id_no):
                self.verified = True
                self.save()
                return True
        return False


class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class District(models.Model):
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name="districts"
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class RegistrationCenter(models.Model):
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, related_name="registration_centers"
    )

    name = models.CharField(max_length=300)
    code = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Duration(models.Model):
    start = models.TimeField()
    end = models.TimeField()

    def __str__(self):
        return f"from : {self.start} to {self.end}"


class RegistrationCenterWorkDay(models.Model):
    registration_center = models.ForeignKey(
        RegistrationCenter, on_delete=models.CASCADE, related_name="registration_days"
    )
    day = models.DateField()


NUMBER_OF_APPOINTMENTS_LIMIT = 1


class AppointmentSlot(models.Model):
    duration = models.ForeignKey(
        Duration, on_delete=models.CASCADE, related_name="appointment_slots"
    )
    registration_center_work_day = models.ForeignKey(
        RegistrationCenterWorkDay,
        on_delete=models.CASCADE,
        related_name="appointment_slots",
    )

    def __str__(self):
        return f"Center: {self.registration_center_work_day.regitration_center} Day: {self.registration_center_work_day.day} duration: {self.duration}"

    def is_full(self):
        return len(self.appointments.all()) >= NUMBER_OF_APPOINTMENTS_LIMIT


class Appointment(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="appointment"
    )
    appointment_option = models.ForeignKey(
        AppointmentSlot, related_name="appointments", on_delete=models.CASCADE
    )
    attempts = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Appintment by {self.user} {self.appointment_option}"

    def save(self, *args, **kwargs):
        if self.appointment_option.is_full():
            raise Exception(
                "Cannot save appointment because appointment_option is full"
            )
        super().save(*args, **kwargs)


#   SIGNALS
# -------------------------------------------------
def create_new_profile(sender, instance, created=False, **kwargs):
    """
    Signal Handler to create a profile for any user as soon as the user is created.
    It creates a new profile only if there is no other profile for that user
    """
    if created:
        UserProfile.objects.get_or_create(user=instance)


def generate_api_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Generate an authentication Token for the newly created user
    """
    if created:
        Token.objects.get_or_create(user=instance)


def create_appointment_options(sender, instance=None, created=False, **kwargs):
    """
    Create appointment_options as soon as RegistrationCenterWorkDay is created
    """
    if created:
        for duration in Duration.objects.all():
            AppointmentSlot.objects.get_or_create(
                duration=duration, registration_center_work_day=instance
            )


# connect the signal to the handler
post_save.connect(create_new_profile, sender=User)
post_save.connect(generate_api_auth_token, sender=User)
post_save.connect(create_appointment_options, sender=RegistrationCenterWorkDay)
