from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import re
from django.db.models import Q
from django.http import HttpRequest
from main.models import  Student, StudentCourse, Status, Address
from BaseView import *
from .serializers import *
class StudentView(BaseView):
    def __init__(self, model=Student, param_name="id", serializer=StudentSerializer):
        super().__init__(model, param_name, serializer)
        self.disability_mapping = {
            "Não PCD": "Nenhum",
            "Física": "Deficiência Física",
            "Auditiva/surdez": "Surdez",
            "Visual": "Deficiência Visual",
            "Outra": "Outro",
            "Múltipla": "Múltiplas Deficiências",
        }

        self.campus_mapping = {
            "JARAGUÁ RAU": "Instituto Federal de Santa Catarina - Campus Jaraguá do Sul - Rau",
        }

    def get(self, request: HttpRequest, pk: str = None) -> Response:
        return super().get(request, pk, False)
        

    def post(self, request: HttpRequest) -> Response:
        if 'post' not in self.allowed_methods:
            return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if not self.is_allowed(request):
            return self.not_allowed_response("You can not Post")

        elif not request.user.is_authenticated:
            return Response({"error": f"You must be logged in to post a/an{self.model.__name__}"}, status=status.HTTP_403_FORBIDDEN)
      
        # Check if the data is a list or a single dictionary
        if isinstance(request.data, list):
            items = request.data
        elif isinstance(request.data, dict):
            # If it's a single JSON object, wrap it in a list
            items = [request.data]
        else:
            return Response({"error": "Expected a list or a single item"}, status=status.HTTP_400_BAD_REQUEST)

    # content_type = request.content_type

        if request.content_type == 'application/json':
            is_bulk = isinstance(request.data, list)
            serializer = self.serializer(data=request.data, many=is_bulk)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            for row in items:
                try:
                    birth_date = row.get('mes_ano_nascimento')
                    disability = row.get('Deficiencia')
                    color_race = row.get('Cor_Raca')
                    father_name = row.get('nome_pai')
                    neighborhood = row.get('bairro')
                    address = row.get('logradouro')
                    city = row.get('municipio')
                    campus = row.get('campus')
                    name = row.get('name')

                    if not all([birth_date, father_name]):
                        # Skip rows with missing fields
                        continue
                    if name:
                        if (father_name):
                            students_with_same_details = self.model.objects.filter(name=name, father_name=father_name, birth_date=birth_date, campus=campus)
                        else:
                            students_with_same_details = self.model.objects.filter(name=name, birth_date=birth_date, campus=campus)
                    elif (father_name):
                        students_with_same_details = self.model.objects.filter(father_name=father_name, birth_date=birth_date, campus=campus)
                    else:
                        students_with_same_details = self.model.objects.filter(birth_date=birth_date, campus=campus)
                    
                    if students_with_same_details.exists():
                        continue
                        #return Response({"error": "Student with the same name already exists"}, status=status.HTTP_400_BAD_REQUEST)

                    if disability in self.disability_mapping:
                        disability = self.disability_mapping[disability]

                    if campus in self.campus_mapping:
                            campus = self.campus_mapping[campus]

                    student = Student.objects.create(
                        father_name=father_name,
                        disability=disability,
                        color_race=color_race,
                        campus=campus
                    )
                    if address and neighborhood and city:
                        cityObject = City.objects.get(name=city)
                        if cityObject:
                            adressObject = Address.objects.create(address=address, neighborhood=neighborhood, city=cityObject)
                            student.address = adressObject

                    # Salvar o objeto Student
                    student.save()

                except Exception as e:
                    return Response({'error': 'Error while processing row: {}'.format(str(e))}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: HttpRequest, pk: str = None) -> Response:
        return super().put(request, pk)

    def delete(self, request: HttpRequest, pk: str = None) -> Response:
        return super().delete(request, pk)


class SearchStudentFilterView(APIView):

    def get(self, request: HttpRequest) -> Response:
        search_query = request.query_params.get('search', '')
        studant = Student.objects.filter(
            Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query | Q(social_name__icontains = search_query | Q(registration__icontains = search_query))) )

        studants_serializer = StudentSerializer(studant, many=True)

        serialized_data = {
            'student': studants_serializer.data,
        }
        return Response(serialized_data, status=status.HTTP_200_OK)
    
class StudentsByAttributeView(BaseView):

    def __init__(self, model=Student, param_name="attribute", serializer=StudentSerializer, allowed_methods=['get']):
        super().__init__(model, param_name, serializer, allowed_methods)

    def get(self, request: HttpRequest, pk: str = None) -> Response:
        return super().get(request, pk, False)

class StudentsByGender(StudentsByAttributeView):

    def __init__(self):
        super().__init__(model=Student, param_name="gender", serializer=StudentSerializer)

class StudentsBySex(StudentsByAttributeView):

    def __init__(self):
        super().__init__(model=Student, param_name="sex", serializer=StudentSerializer)

class StudentsByColorRace(StudentsByAttributeView):

    def __init__(self):
        super().__init__(model=Student, param_name="color_race", serializer=StudentSerializer)

class StudentsByDisability(StudentsByAttributeView):

    def __init__(self):
        super().__init__(model=Student, param_name="disability", serializer=StudentSerializer)

class StudentsByMother(StudentsByAttributeView):

    def __init__(self):
        super().__init__(model=Student, param_name="mother", serializer=StudentSerializer)

class StudentsByFather(StudentsByAttributeView):
    
    def __init__(self):
        super().__init__(model=Student, param_name="father", serializer=StudentSerializer)


class StudentsByCity(APIView):

    def get(self, request: HttpRequest, city: str = None, id: int = None) -> Response:
        if not int:
            int = request.data.get('int')
        if not city:
            city = request.data.get('city')
        object = Student.objects.filter(int=int, address__city=city)
        if object:
            serializer = StudentSerializer(object, many=True)
            return Response({"students": serializer.data}, status=status.HTTP_200_OK)
        return Response({"students": None}, status=status.HTTP_200_OK)


class StudentsByInstitute(APIView):

    def get(self, request: HttpRequest, institute: str = None, id: int = None) -> Response:
        if not id:
            id = request.data.get('id')
        if not institute:
            institute = request.data.get('institute')
        object = Student.objects.filter(id=id, institute=institute)
        if object:
            serializer = StudentSerializer(object, many=True)
            return Response({"students": serializer.data}, status=status.HTTP_200_OK)
        return Response({"students": None}, status=status.HTTP_200_OK)


class StudentsByPreviousSchool(APIView):

    def get(self, request: HttpRequest, previous_school: str = None, id: int = None) -> Response:
        if not id:
            id = request.data.get('id')
        if not previous_school:
            previous_school = request.data.get('previous_school')
        object = Student.objects.filter(id=id, previous_school=previous_school)
        if object:
            serializer = StudentSerializer(object, many=True)
            return Response({"students": serializer.data}, status=status.HTTP_200_OK)
        return Response({"students": None}, status=status.HTTP_200_OK)


class StudentsByCourse(APIView):

    def get(self, request: HttpRequest, course: int = None, id: int = None) -> Response:
        if not id:
            id = request.data.get('id')
        if not course:
            course = request.data.get('course')
        object = StudentCourse.objects.filter(id=id, course=course)
        if object:
            serializer = StudentCourseSerializer(object, many=True)
            return Response({"students": serializer.data}, status=status.HTTP_200_OK)
        return Response({"students": None}, status=status.HTTP_200_OK)


class StudentCourseView(BaseView):
    def __init__(self, model=StudentCourse, param_name="id", serializer=StudentCourse):
        super().__init__(model, param_name, serializer)

    def get(self, request: HttpRequest, pk: str = None) -> Response:
        return super().get(request, pk, False)

    def post(self, request: HttpRequest) -> Response:
        return super().post(request)

    def put(self, request: HttpRequest, pk: str = None) -> Response:
        return super().put(request, pk)

    def delete(self, request: HttpRequest, pk: str = None) -> Response:
        return super().delete(request, pk)

class StatusView(BaseView):
    def __init__(self, model=Status, param_name="id", serializer=StatusSerializer):
        super().__init__(model, param_name, serializer)

    def get(self, request: HttpRequest, pk: str = None) -> Response:
        return super().get(request, pk, False)

    def post(self, request: HttpRequest) -> Response:
        return super().post(request)

    def put(self, request: HttpRequest, pk: str = None) -> Response:
        return super().put(request, pk)

    def delete(self, request: HttpRequest, pk: str = None) -> Response:
        return super().delete(request, pk)

