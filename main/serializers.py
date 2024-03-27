from rest_framework import serializers
from .models import CustomUser, City, Address, Institute, PreviousSchool, Course, Student, StudentCourse, Status
import random
class BulkSerializerMixin:
    def to_internal_value(self, data):
        if isinstance(data, list):
            return [super().to_internal_value(item) for item in data]
        return super().to_internal_value(data)
    def create(self, validated_data):
        if isinstance(validated_data, list):
            return [self.Meta.model.objects.create(**item) for item in validated_data]
        return self.Meta.model.objects.create(**validated_data)
class CitySerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class AddressSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), pk_field=serializers.CharField())

    class Meta:
        model = Address
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        city_serializer = CitySerializer(instance.city)
        representation['city'] = city_serializer.data
        return representation
    
class InstituteSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Institute
        fields = '__all__'

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address = AddressSerializer().create(validated_data=address_data)
        institute = Institute.objects.create(address=address, **validated_data)
        return institute

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address')
        address_serializer = AddressSerializer(instance.address, data=address_data)
        if address_serializer.is_valid():
            address_serializer.save()  # Save the nested address
        instance.name = validated_data.get('name', instance.name)
        # Update other fields of Institute if necessary
        instance.save()
        return instance






























class PreviousSchoolSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = PreviousSchool
        fields = '__all__'


class CourseSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class CustomUserSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['is_staff', 'groups', 'user_permissions',
                   'last_login', 'date_joined', 'is_active']


class CustomUserListSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name',
                  'profile_picture', 'sex', 'gender', 'birth_date', 'created_at', 'updated_at', 'password']


class CurrentCustomUserSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'pseudo_name',
        fields = '__all__'
        # 'profile_picture', 'sex', 'gender', 'bio', 'birth_date', 'created_at', 'updated_at',]
