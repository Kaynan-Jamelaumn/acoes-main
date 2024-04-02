from django.urls import path
from .views import (
    CurrentUserView,
    CustomUserView,
    CustomUserLogin,
    CustomUserLogout,
    CityView,
    AddressView,
    InstituteView,
    InstitutePageView,
    PreviousSchoolView,
    CourseView,
)

urlpatterns = [
    path('user/current/', CurrentUserView.as_view(), name='current-user'),
    path('user/', CustomUserView.as_view(), name='user-list'),
    path('user/login/', CustomUserLogin.as_view(), name='user-login'),
    path('user/logout/', CustomUserLogout.as_view(), name='user-logout'),
    path('user/<int:pk>/', CustomUserView.as_view(), name='user-detail'),

    path('city/', CityView.as_view(), name='city-list'),
    path('city/<str:pk>/', CityView.as_view(), name='city-detail'),

    path('address/', AddressView.as_view(), name='address-list'),
    path('address/<int:pk>/', AddressView.as_view(), name='address-detail'),

    path('institute/', InstituteView.as_view(), name='institute-list'),
    path('institute/<str:pk>/', InstituteView.as_view(), name='institute-detail'),
    path('institute-page/', InstitutePageView.as_view(), name='institute-page-list'),
    path('institute-page/<int:page>/', InstitutePageView.as_view(), name='institute-page'),

    path('previous-school/', PreviousSchoolView.as_view(),
         name='previous-school-list'),
    path('previous-school/<str:pk>/', PreviousSchoolView.as_view(),
         name='previous-school-detail'),

    path('course/', CourseView.as_view(), name='course-list'),
    path('course/<int:pk>/', CourseView.as_view(), name='course-detail'),

]
