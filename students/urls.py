from .views import (    
    StudentView,
    StudentPageView,
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
    StudentsByCourse,
    StudentCourse_Status_View,
    StudentCoursePageView,
    StatusPageView,
    )
from django.urls import path



urlpatterns = [
    path('student/', StudentView.as_view(), name='student-list'),
    path('student/<int:pk>/', StudentView.as_view(), name='student-detail'),

    path('student-page/', StudentPageView.as_view(), name='student-page-list'),
    path('student-page/<int:page>/', StudentPageView.as_view(), name='student-detail'),

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

     path('studentcourse-status/',
         StudentCourse_Status_View.as_view(), name='student-bulk'),

    path('studentcourse-page/', StudentCoursePageView.as_view(), name='student-page-list'),
    path('studentcourse-page/<int:page>/', StudentCoursePageView.as_view(), name='student-detail'),

    path('status-page/', StatusPageView.as_view(), name='student-page-list'),
    path('status-page/<int:page>/', StatusPageView.as_view(), name='student-detail'),


]
