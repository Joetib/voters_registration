from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path("user/", views.UserDetailView.as_view(), name="user-detail"),
    path("user/profile/", views.ProfileUpdateView.as_view(), name="profile"),
    path("regions/", views.RegionListView.as_view(), name="region-list-all"),
    path("regions/<int:region_id>/districts/", views.DistrictInRegionListView.as_view(), name="district-list-all"),
    path(
        "district/<int:district_id>/registration-centers/",
        views.RegistrationCenterInDistrictListView.as_view(),
        name="all-registration-centers",
    ),
    path(
        "registration-center/<int:registration_center_id>/available-days/",
        views.RegistrationCenterWorkDayListView.as_view(),
        name="all-available-appointments",
    ),
    path(
        "registration-center/<int:registration_center_id>/day/<int:day_id>/slots/available/",
        views.AvailableAppointmentInRegistrationCenterDayView.as_view(),
        name="all-available-appointments",
    ),
    path(
        "appointment/create/",
        views.CreateAppointmentView.as_view(),
        name="create-appointment",
    ),
    path(
        "appointment/",
        views.AppointmentDetailView.as_view(),
        name="appointment-detail",
    ),
]
