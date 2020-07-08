from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Region)
admin.site.register(models.District)
admin.site.register(models.RegistrationCenter)
admin.site.register(models.UserProfile)
admin.site.register(models.Appointment)
admin.site.register(models.AppointmentSlot)
admin.site.register(models.RegistrationCenterWorkDay)
admin.site.register(models.Duration)