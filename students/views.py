from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import re
from django.db.models import Q
from django.http import HttpRequest
from main.models import  Student, StudentCourse, Status, Address, Course, Institute, PreviousSchool
from BaseView import *
from .serializers import *
import datetime
from itertools import islice


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
        self.school_mapping = {
            "PRIVADA"
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
                    previous_school_type = row.get('Tipo de escola que concluiu o Ensino Médio')

                    if not all([birth_date, father_name]):
                        # Skip rows with missing fields
                        continue

                    if campus in self.campus_mapping:
                        campus = self.campus_mapping[campus]
                    campus_regex = r'\b{}\b'.format(re.escape(campus.lower()))

                    # Filter the Institute using the regular expression
                    institute_object = Institute.objects.filter(name__iregex=campus_regex).first()          
                    birth_date_parts = birth_date.split('/')
                    if len(birth_date_parts) == 2:
                        year = int(birth_date_parts[1])
                        month = int(birth_date_parts[0])
                        # Defina o dia como 1, pois você não tem essa informação
                        day = 1
                        birth_date = datetime.date(year, month, day)
                    else:
                        raise ValueError("Formato de data inválido")


                    if name:
                        if (father_name):
                            students_with_same_details = self.model.objects.filter(name=name, father_name=father_name, birth_date=birth_date, institute=institute_object)
                        else:
                            students_with_same_details = self.model.objects.filter(name=name, birth_date=birth_date, institute=institute_object)
                    elif (father_name):
                        students_with_same_details = self.model.objects.filter(father_name=father_name, birth_date=birth_date, institute=institute_object)
                    else:
                        students_with_same_details = self.model.objects.filter(birth_date=birth_date, institute=institute_object)
                    
                    if students_with_same_details.exists():
                        student = students_with_same_details.first()

                    
                    else:
                        if disability in self.disability_mapping:
                            disability = self.disability_mapping[disability]

                        if previous_school_type in self.school_type_mapping:
                            previous_school_type = self.school_type_mapping[previous_school_type]
                        #previous_school_object = PreviousSchool.objects.create(type=previous_school_type)
                        student = Student.objects.create(
                            father_name=father_name,
                            disability=disability,
                            color_race=color_race,
                            institute=institute_object,
                            school_type = previous_school_type,
                            birth_date = birth_date,
                        )
                        if address and neighborhood and city and city !='NÃO INFORMADO':
                            # try:
                            cityObject, created = City.objects.get_or_create(name=city)
                            addressObject = Address.objects.create(address=address, neighborhood=neighborhood, city=cityObject)
                            student.address = addressObject
                            # except City.DoesNotExist:
                            #     # Handle the error - log it, or return a response indicating which city was not found
                            #     return Response({'error': f'City "{city}" not found in the database.'}, status=status.HTTP_400_BAD_REQUEST)
                            # cityObject = City.objects.get(name=city)
                            # if not cityObject: print("aa")
                            # if cityObject:
                            #     adressObject = Address.objects.create(address=address, neighborhood=neighborhood, city=cityObject)
                            #     student.address = adressObject

                        # Salvar o objeto Student
                        student.save()

                except Exception as e:
                    return Response({'error': 'Error while processing row: {}'.format(str(e))}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Data processed successfully"}, status=status.HTTP_200_OK)


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


class Student_Course_Status_View(BaseView):
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
        self.status_mapping = {
            "CANCELADO" : 'Cancelado',
            "CURSANDO" : 'Cursando',
            "CONCLUÍDO" : 'Concluído',
            "TRANCADO" : 'Trancado',
        }

        self.campus_mapping = {
            "JARAGUÁ RAU": "Instituto Federal de Santa Catarina - Campus Jaraguá do Sul - Rau",
        }
        self.school_type_mapping = {
            'Educação de Jovens e Adultos (EJA)': 'EJA',
            'Técnico Integrado': 'Técnico Integrado',
            'Técnico Subsequente': 'Técnico Subsequente',
            'Tecnólogo': 'Tecnólogo',
            'Bacharelado': 'Bacharelado',
            'Licenciatura': 'Licenciatura',
            'PRIVADA' : 'Privada',
            'ESTADUAL' : 'Estadual',
            'MUNICIPAL' : 'Municipal',
            'COMUNITÁRIA' : 'Comunitiária',
            'FEDERAL' : 'Federal',
            'OUTRA' : 'Outra',
        }
        self.admission_process_mapping = {
            'Não Cotista' : 'Competição geral',
            'Escola Pública e PPI' : 'Escola Pública + PPI',
            'Escola Pública e Renda' : 'Escola Pública + Renda até 1,5 vezes o salário mínimo per capita',
            'Escola Pública, PCD' : 'Escola Pública + PCD',
            'Escola Pública, Renda e PCD' : 'Escola Pública + PCD + Renda até 1,5 vezes o salário mínimo per capita',
            'Escola Pública, Renda e PPI' : 'Escola Pública + PPI + Renda até 1,5 vezes o salário mínimo per capita',
            'Escola Pública, Renda, PCD e PPI' : 'Escola Pública + PCD + PPI + Renda até 1,5 vezes o salário mínimo per capita',
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
                    previous_school_type = row.get('Tipo de escola que concluiu o Ensino Médio')

                    ingressed_semester = row.get('semestre_ingresso')
                    student_status = row.get('Status')

                    admission_process = row.get('Cota')

                    year_created = row.get('ano_ingresso')
                    course = row.get('Curso')
                    modality = row.get('modalidade')
                    shift = row.get('turno')
                    time_required = row.get('Tempo_min_Integralizacao_Curso')
                    course_type = row.get('Tipo de Curso')

                    if not all([year_created, course, campus, modality, shift, time_required, course_type,birth_date, father_name]):
                        # Skip rows with missing fields
                        continue

                    # Converta "MM/YYYY" para "YYYY-MM-DD"

                    if campus in self.campus_mapping:
                        campus = self.campus_mapping[campus]
                    campus_regex = r'\b{}\b'.format(re.escape(campus.lower()))

                    # Filter the Institute using the regular expression
                    institute_object = Institute.objects.filter(name__iregex=campus_regex).first()
                                        
                    course_object, created= Course.objects.get_or_create(
                        year_created=year_created,
                        name=course,
                        institute=institute_object,
                        modality=modality,
                        shift=shift,
                        type=course_type,
                        time_required=time_required
                    )
                                        
                    birth_date_parts = birth_date.split('/')
                    if len(birth_date_parts) == 2:
                        year = int(birth_date_parts[1])
                        month = int(birth_date_parts[0])
                        # Defina o dia como 1, pois você não tem essa informação
                        day = 1
                        birth_date = datetime.date(year, month, day)
                    else:
                        raise ValueError("Formato de data inválido")


                    if name:
                        if (father_name):
                            students_with_same_details = self.model.objects.filter(name=name, father_name=father_name, birth_date=birth_date, institute=institute_object)
                        else:
                            students_with_same_details = self.model.objects.filter(name=name, birth_date=birth_date, institute=institute_object)
                    elif (father_name):
                        students_with_same_details = self.model.objects.filter(father_name=father_name, birth_date=birth_date, institute=institute_object)
                    else:
                        students_with_same_details = self.model.objects.filter(birth_date=birth_date, institute=institute_object)
                    
                    if students_with_same_details.exists():
                        student = students_with_same_details.first()

                    
                    else:
                        if disability in self.disability_mapping:
                            disability = self.disability_mapping[disability]

                        if previous_school_type in self.school_type_mapping:
                            previous_school_type = self.school_type_mapping[previous_school_type]
                        #previous_school_object = PreviousSchool.objects.create(type=previous_school_type)
                        student = Student.objects.create(
                            father_name=father_name,
                            disability=disability,
                            color_race=color_race,
                            institute=institute_object,
                            school_type = previous_school_type,
                            birth_date = birth_date,
                        )
                        if address and neighborhood and city and city !='NÃO INFORMADO':
                            # try:
                            cityObject, created = City.objects.get_or_create(name=city)
                            addressObject = Address.objects.create(address=address, neighborhood=neighborhood, city=cityObject)
                            student.address = addressObject
                            # except City.DoesNotExist:
                            #     # Handle the error - log it, or return a response indicating which city was not found
                            #     return Response({'error': f'City "{city}" not found in the database.'}, status=status.HTTP_400_BAD_REQUEST)
                            # cityObject = City.objects.get(name=city)
                            # if not cityObject: print("aa")
                            # if cityObject:
                            #     adressObject = Address.objects.create(address=address, neighborhood=neighborhood, city=cityObject)
                            #     student.address = adressObject

                        # Salvar o objeto Student
                        student.save()

                    if admission_process in self.admission_process_mapping:
                        admission_process = self.admission_process_mapping[admission_process]
                    student_course_object, created =  StudentCourse.objects.get_or_create(
                        student=student,
                        course=course_object,
                        ingressed_semester= ingressed_semester,
                        admission_process=admission_process
                    )
                    if student_status in self.status_mapping:
                        student_status = self.status_mapping[student_status]


                    status_object = Status.objects.create(
                        student_course=student_course_object,
                        status = student_status
                    )

                except Exception as e:
                    return Response({'error': 'Error while processing row: {}'.format(str(e))}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': 'Data processed successfully!'}, status=status.HTTP_200_OK)

    def put(self, request: HttpRequest, pk: str = None) -> Response:
        return super().put(request, pk)

    def delete(self, request: HttpRequest, pk: str = None) -> Response:
        return super().delete(request, pk)
