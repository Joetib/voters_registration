from application.models import Appointment
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer,CharField, ModelSerializer, ImageField
from django.contrib.auth import get_user_model


from . import models

User = get_user_model()


class ProfileSerializer(ModelSerializer):
    picture = ImageField(allow_empty_file=True, allow_null=True, required=False, use_url=True)

    class Meta:
        model = models.UserProfile
        fields = ('id','verified','picture', 'national_id_no')

    
    def update(self, instance, validated_data, *args, **kwargs):
        if instance.verified != validated_data['verified']:
            raise ValidationError('Cannot Change National Id no after it is validated')

        if instance.verified and instance.national_id_no and instance.national_id_no != validated_data['national_id_no']:
            raise ValidationError('Cannot Change National Id no after it is validated')
        instance.picture = validated_data['picture']
        instance.national_id_no = validated_data['national_id_no']
        instance.save()
        return instance
    


class CreateUserSerializer(ModelSerializer):
    class Meta:
        fields = ('username', 'password')
        model = User

class UserDetailSerializer(ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ('id','username', 'email', 'first_name', 'last_name', 'profile')

    

class UserUpdateSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('id','email','first_name', 'last_name')
    

class RegistrationCenterSerializer(ModelSerializer):
    class Meta:
        fields = ('id','name', 'district', 'code')
        model = models.RegistrationCenter

class DistrictSerializer(ModelSerializer):
    registration_centers = RegistrationCenterSerializer(many=True)

    class Meta:
        model = models.District
        fields = ('__all__')
  



class RegionSerializer(ModelSerializer):
    districts = DistrictSerializer(many=True)
    class Meta:
        model = models.Region
        fields = ('__all__')

class DurationSerializer(ModelSerializer):
    class Meta:
        model = models.Duration
        fields = ('id','start', 'end')

class RegistrationCenterWorkDaySerializer(ModelSerializer):
    registration_center = RegistrationCenterSerializer()
    class Meta:
        model = models.RegistrationCenterWorkDay
        fields = ('id', 'registration_center', 'day')

class AppointmentSlotSerializer(ModelSerializer):
    registration_center_work_day  = RegistrationCenterWorkDaySerializer()
    duration = DurationSerializer()
    class Meta:
        model = models.AppointmentSlot
        fields = ('id', 'registration_center_work_day', 'duration')

class AppointmentSlotSerializer2(ModelSerializer):
    
    class Meta:
        model = models.AppointmentSlot
        fields = ('id')

class AppointmentSerializer(ModelSerializer):
    class Meta:
        model = models.Appointment
        fields = ('appointment_slot', 'attempts')

    def create(self, validated_data, user=None):
        if user:
            appointment_qs = Appointment.objects.filter(user=user)
            if appointment_qs.exists():
                appointment = appointment_qs[0]
                appointment.appointment_slot = validated_data['appointment_slot']
                appointment.attempts += 1
                appointment.save()
            else:
                appointment = Appointment.objects.create(user=user, appointment_slot=validated_data['appointment_slot'])
        else:
            appointment = super().create(validated_data)
        return appointment
