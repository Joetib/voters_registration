from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('create-user/', views.CreateUser.as_view(), name="create-user"),
    path('user/<int:pk>/', views.UserDetailView.as_view(), name="user-detail"),
    path('user/profile/', views.ProfileUpdateView.as_view(), name="profile"),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('registration-centers/all/', views.RegistrationCenterListView.as_view(), name="all-registration-centers"),
    path('districts/all/', views.DistrictListView.as_view(), name="district-list-all"),
    path('regions/all/', views.RegionListView.as_view(), name="region-list-all"),
    path('slots/all/', views.AllAvailableAppointment.as_view(), name="all-available-appointments"),
]