from django.utils import timezone
from rest_framework.serializers import Serializer
from application.models import (
    District,
    AppointmentSlot,
    Appointment,
    Region,
    RegistrationCenter,
    RegistrationCenterWorkDay,
    UserProfile,
)
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from . import serializers
from datetime import date

# Create your views here.

User = get_user_model()




class ProfileUpdateView(APIView):
    """
    Update the Profile of the current User

    Data : 
        * Verified
        * picture
        * National_id_no

        If the profile is already verified, you cannot and must not try to change the 
        national_id_no field. 
        Neither should you make any attempt to modify a profile's verified property.
        
    """

    permissions = [IsAuthenticated]
    serializer_class = serializers.ProfileSerializer

    def get(self, request, *args, **kwargs):
        return Response(serializers.ProfileSerializer(request.user.profile).data)

    def put(self, request, *args, **kwargs):
        serializer = serializers.ProfileSerializer(
            request.user.profile, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_304_NOT_MODIFIED)


class UserDetailView(APIView):
    """
    Gets and updates User profile details
    """
    permissions = [IsAuthenticated]
    serializer_class = serializers.UserDetailSerializer

    def get(self, request, *args, **kwargs):
        serializer = serializers.UserDetailSerializer(request.user)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):

        serializer = serializers.UserDetailSerializer(
            instance=request.user, data=request.data
        )
        if serializer.is_valid():
            try:
                serializer.save()
            except ValidationError as e:
                return Response(
                    {"error": True, "message": e}, status=status.HTTP_409_CONFLICT
                )
            return Response(serializer.data)
        return Response(serializer.errors)


class RegionListView(generics.ListAPIView):
    """
    List of all Regions
    """
    serializer_class = serializers.RegionSerializer

    def get_queryset(self, *args, **kwargs):
        return Region.objects.all()

class DistrictInRegionListView(generics.ListAPIView):
    """
    List of all Districts
    """
    serializer_class = serializers.DistrictSerializer

    def get_queryset(self, *args, **kwargs):
        region_id = self.kwargs['region_id']
        region = get_object_or_404(Region, id=region_id)
        return District.objects.filter(region=region)

class RegistrationCenterWorkDayListView(generics.ListAPIView):
    """
    List of all Days that work will be done in a registration center

    You need to pass in the id of the registration center
    """
    serializer_class = serializers.RegistrationCenterWorkDaySerializer

    def get_queryset(self, *args, **kwargs):
        registration_center_id = self.kwargs['registration_center_id']
        registration_center = get_object_or_404(RegistrationCenter, id=registration_center_id)
        return RegistrationCenterWorkDay.objects.filter(registration_center=registration_center)


class RegistrationCenterInDistrictListView(generics.ListAPIView):
    """
    List of all registration centers
    """
    serializer_class = serializers.RegistrationCenterSerializer

    def get_queryset(self, *args, **kwargs):
        district_id = self.kwargs['district_id']
        district = get_object_or_404(District, id=district_id)
        return RegistrationCenter.objects.filter(district=district)


class AvailableAppointmentInRegistrationCenterDayView(generics.ListAPIView):
    """
    Get a list of all available appointment slots in District on a particular day
    """
    serializer_class = serializers.AppointmentSlotSerializer

    def get_queryset(self):
        day_id = self.kwargs["day_id"]

        day_qs = RegistrationCenterWorkDay.objects.filter(
            day__gte=date.today(), id=day_id,
        )
        if day_qs.exists():
            day = day_qs[0]

        else:
            print(">>> ", "Day does not exist")
            return []

        appointmentslots = AppointmentSlot.objects.filter(
             registration_center_work_day=day,
        )
        print(appointmentslots)
        appointmentslots = [
            appointmentslot
            for appointmentslot in appointmentslots
            if not appointmentslot.is_full()
        ]
        return appointmentslots

class CreateAppointmentView(APIView):
    """
    Create a new Appointment
    """
    serializer_class = serializers.AppointmentSerializer
    permissions = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = serializers.AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.create(
                user=request.user, validated_data=serializer.validated_data
            )
            data = serializer.data
            data['id'] = instance.id
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class AppointmentDetailView(generics.GenericAPIView):
    """
    Gets and modifies an appointment made by the current user

    methods allowed:
        * Get
        * Put

    """
    serializer_class = serializers.AppointmentSerializer
    permissions = [IsAuthenticated]

    def get_queryset_1(self):
        appointment_qs = Appointment.objects.filter(user=self.request.user)
        if appointment_qs.exists():
            appointment = appointment_qs[0]
            return appointment
        return None

    def get(self, request, *args, **kwargs):
        user_appointment = self.get_queryset_1()
        if user_appointment:
            serializer = serializers.AppointmentDetailSerializer(user_appointment)
            return Response(serializer.data)
        return Response({"error": True, "message": "User has no appointment"})
    
    def put(self, request, *args, **kwargs):
        user_appointment = self.get_queryset_1()
        if user_appointment:
            serializer = serializers.AppointmentSerializer(
                user_appointment, data=request.data
            )
            if serializer.is_valid():
                appointment = serializer.save()
                serializer = serializers.AppointmentDetailSerializer(appointment)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_304_NOT_MODIFIED)
        return Response({"error": True, "message": "User has no appointment"}, status=status.HTTP_304_NOT_MODIFIED)

