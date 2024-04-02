from rest_framework import serializers
from main.models import City, Student, StudentCourse, Status
from main.serializers import CourseSerializer, PreviousSchoolSerializer, InstituteSerializer
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
class StatusSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class StudentSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    institute = InstituteSerializer()
   # previous_school = PreviousSchoolSerializer()

    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        name = validated_data.get('name')
        father_name = validated_data.get('father_name')
        birth_date = validated_data.get('birth_date')
        campus = validated_data.get('campus')

        if name:
            if father_name:
                students_with_same_details = self.Meta.model.objects.filter(name=name, father_name=father_name, birth_date=birth_date, campus=campus)
            else:
                students_with_same_details = self.Meta.model.objects.filter(name=name, birth_date=birth_date, campus=campus)
        elif father_name:
            students_with_same_details = self.Meta.model.objects.filter(father_name=father_name, birth_date=birth_date, campus=campus)
        else:
            students_with_same_details = self.Meta.model.objects.filter(birth_date=birth_date, campus=campus)
        
        if students_with_same_details.exists():
            raise serializers.ValidationError("This student already exists")

        return super().create(validated_data)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Dicionários de mapeamento de nomes aleatórios com base no sexo
        male_names = {
            'Batman',
            'Ninja',
            'Homem Aranha',
            'Rei Macaco',
            'Coringa'
        }
        female_names = {
            'Princesa',
            'Mulan',
            'Rapunzel',
            'Ariel'
        }

        # Verifica o sexo e escolhe um nome aleatório
        if instance.sex == 'Masculino':
            representation['name'] = random.choice(list(male_names))
        elif instance.sex == 'Feminino':
            representation['name'] = random.choice(list(female_names))
        return representation
class StudentCourseSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    student = StudentSerializer()
    course = CourseSerializer()
    status = StatusSerializer()

    class Meta:
        model = StudentCourse
        fields = '__all__'

