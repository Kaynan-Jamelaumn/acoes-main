from django.urls import path
from .views import (
    CurrentUserView,
    CustomUserView,
    CustomUserLogin,
    CustomUserLogout,
    CityView,
    AddressView,
    InstituteView,
    PreviousSchoolView,
    CourseView,
    StudentView,
    SearchStudentFilterView,
    StudentsBySex,
    StudentsByGender,
    StudentsByColorRace,
    StudentsByDisability,
    StudentsByMother,
    StudentsByFather,
    StudentsByInstitute,
    StudentsByPreviousSchool,
    StudentsByCity,
    StudentsByCourse
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

    path('previous-school/', PreviousSchoolView.as_view(),
         name='previous-school-list'),
    path('previous-school/<str:pk>/', PreviousSchoolView.as_view(),
         name='previous-school-detail'),

    path('course/', CourseView.as_view(), name='course-list'),
    path('course/<int:pk>/', CourseView.as_view(), name='course-detail'),

    path('student/', StudentView.as_view(), name='student-list'),
    path('student/<int:pk>/', StudentView.as_view(), name='student-detail'),
    path('search-student/', SearchStudentFilterView.as_view(), name='student-list'),

    path('search-student-by-sex/',
         StudentsBySex.as_view(), name='student-by-sex-list'),
    path('search-student-by-sex/<str:sex>/',
         StudentsBySex.as_view(), name='student-by-sex-detail'),

    path('search-student-by-gender/',
         StudentsByGender.as_view(), name='student-by-gender-list'),
    path('search-student-by-gender/<str:gender>/',
         StudentsByGender.as_view(), name='student-by-gender-detail'),

    path('search-student-by-color-race/',
         StudentsByColorRace.as_view(), name='student-by-color-race-list'),
    path('search-student-by-color-race/<str:color_race>/',
         StudentsByColorRace.as_view(), name='student-by-color-race-detail'),

    path('search-student-by-disability/',
         StudentsByDisability.as_view(), name='student-by-disability-list'),
    path('search-student-by-disability/<str:disability>/',
         StudentsByDisability.as_view(), name='student-by-disability-detail'),

    path('search-student-by-mother/',
         StudentsByMother.as_view(), name='student-by-mother-list'),
    path('search-student-by-mother/<str:mother_name>/',
         StudentsByMother.as_view(), name='student-by-mother-detail'),

    path('search-student-by-father/',
         StudentsByFather.as_view(), name='student-by-father-list'),
    path('search-student-by-father/<str:father_name>/',
         StudentsByFather.as_view(), name='student-by-father-detail'),

    path('search-student-by-institute/',
         StudentsByInstitute.as_view(), name='student-by-institute-list'),
    path('search-student-by-institute/<str:institute>/<int:id>/',
         StudentsByInstitute.as_view(), name='student-by-institute-detail'),

    path('search-student-by-previous-school/',
         StudentsByPreviousSchool.as_view(), name='student-by-previous-school-list'),
    path('search-student-by-previous-school/<str:previous_school>/<int:id>/',
         StudentsByPreviousSchool.as_view(), name='student-by-previous-school-detail'),

    path('search-student-by-city/',
         StudentsByCity.as_view(), name='student-by-city-list'),
    path('search-student-by-city/<str:city>/<int:id>/',
         StudentsByCity.as_view(), name='student-by-city-detail'),

    path('search-student-by-course/',
         StudentsByCourse.as_view(), name='student-by-course-list'),
    path('search-student-by-course/<int:course>/<int:id>/',
         StudentsByCourse.as_view(), name='student-by-course-detail'),




]
