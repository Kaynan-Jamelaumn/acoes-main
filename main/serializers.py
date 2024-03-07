from rest_framework import serializers
from .models import CustomUser, City, Address, Institute, PreviousSchool, Course, Student, StudentCourse, Status


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = Address
        fields = '__all__'


class InstituteSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Institute
        fields = '__all__'


class PreviousSchoolSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = PreviousSchool
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    institute = InstituteSerializer()
    previous_school = PreviousSchoolSerializer()

    class Meta:
        model = Student
        fields = '__all__'


class StudentCourseSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    course = CourseSerializer()
    status = StatusSerializer()

    class Meta:
        model = StudentCourse
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['is_staff', 'groups', 'user_permissions',
                   'last_login', 'date_joined', 'is_active']


class CustomUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name',
                  'profile_picture', 'sex', 'gender', 'birth_date', 'created_at', 'updated_at', 'password']


class CurrentCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'pseudo_name',
        fields = '__all__'
        # 'profile_picture', 'sex', 'gender', 'bio', 'birth_date', 'created_at', 'updated_at',]
