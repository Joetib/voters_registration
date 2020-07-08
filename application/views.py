from application.models import (
    District,
    AppointmentSlot,
    Appointment,
    Region,
    RegistrationCenter,
    UserProfile,
)
from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from . import serializers

# Create your views here.

User = get_user_model()

"""
class CreateUser(generics.CreateAPIView):
    serializer_class = serializers.CreateUserSerializer
"""


class CreateUser(APIView):
    """
    Create a new User.
    Methods accepted : POST
    Post Parameters:
        username : The name of the user to be created
        password : The password of the user
    """

    serializer_class = serializers.CreateUserSerializer

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = User.objects.create_user(username=username, password=password)
        return Response({"Token": user.auth_token})


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
        Wanna fail, try me! (/)(/)
        
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
    serializer_class = serializers.RegionSerializer

    def get_queryset(self, *args, **kwargs):
        return Region.objects.all()


class DistrictListView(generics.ListAPIView):
    serializer_class = serializers.DistrictSerializer

    def get_queryset(self, *args, **kwargs):
        return District.objects.all()


class RegistrationCenterListView(generics.ListAPIView):
    serializer_class = serializers.RegistrationCenterSerializer

    def get_queryset(self, *args, **kwargs):
        return RegistrationCenter.objects.all()


class AllAvailableAppointment(generics.ListAPIView):
    serializer_class = serializers.AppointmentSlotSerializer

    def get_queryset(self):
        appointments = AppointmentSlot.objects.filter(is_full=False)
        return appointments
