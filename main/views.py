from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import re
from django.http import HttpRequest
from django.db.models import Q
from .serializers import CustomUserSerializer, CustomUserListSerializer, CurrentCustomUserSerializer, CitySerializer, AddressSerializer, InstituteSerializer, PreviousSchoolSerializer, CourseSerializer
from .models import CustomUser, City, Address, Institute, PreviousSchool, Course, Student, StudentCourse, Status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from students.views import *

from .models import CustomUser
from BaseView import BaseView
import csv
import pandas as pd
class CityView(BaseView):
    def __init__(self, model=City, param_name="name", serializer=CitySerializer):
        super().__init__(model, param_name, serializer)

    def get(self, request: HttpRequest, pk: str = None) -> Response:
        return super().get(request, pk, False)

    def post(self, request: HttpRequest) -> Response:
        return super().post(request)

    def put(self, request: HttpRequest, pk: str = None) -> Response:
        return super().put(request, pk)

    def delete(self, request: HttpRequest, pk: str = None) -> Response:
        return super().delete(request, pk)


class AddressView(BaseView):
    def __init__(self, model=Address, param_name="id", serializer=AddressSerializer):
        super().__init__(model, param_name, serializer)

    def get(self, request: HttpRequest, pk: str = None) -> Response:
        return super().get(request, pk, False)

    def post(self, request: HttpRequest) -> Response:
        return super().post(request)

    def put(self, request: HttpRequest, pk: str = None) -> Response:
        return super().put(request, pk)

    def delete(self, request: HttpRequest, pk: str = None) -> Response:
        return super().delete(request, pk)


class InstituteView(BaseView):
    def __init__(self, model=Institute, param_name="name", serializer=InstituteSerializer):
        super().__init__(model, param_name, serializer)

    def get(self, request: HttpRequest, pk: str = None) -> Response:
        return super().get(request, pk, False)

    def post(self, request: HttpRequest) -> Response:
        return super().post(request)

    def put(self, request: HttpRequest, pk: str = None) -> Response:
        return super().put(request, pk)

    def delete(self, request: HttpRequest, pk: str = None) -> Response:
        return super().delete(request, pk)




class PreviousSchoolView(BaseView):
    def __init__(self, model=PreviousSchool, param_name="name", serializer=PreviousSchoolSerializer):
        super().__init__(model, param_name, serializer)

    def get_type_from_name(name):
        TYPE_MAPPING = {
            'Educação de Jovens e Adultos (EJA)': ['EJA'],
            'Técnico Integrado': ['Técnico Integrado'],
            'Técnico Subsequente': ['Técnico Subsequente'],
            'Tecnólogo': ['Tecnólogo'],
            'Bacharelado': ['Bacharelado'],
            'Licenciatura': ['Licenciatura']
        }

        for key, value in TYPE_MAPPING.items():
            for keyword in value:
                if keyword.lower() in name.lower():
                    return key
        return None
    def get(self, request: HttpRequest, pk: str = None) -> Response:
        return super().get(request, pk, False)

    def post(self, request: HttpRequest) -> Response:
        return super().post(request)
    def put(self, request: HttpRequest, pk: str = None) -> Response:
        return super().put(request, pk)

    def delete(self, request: HttpRequest, pk: str = None) -> Response:
        return super().delete(request, pk)


class CourseView(BaseView):
    
    def __init__(self, model=Course, param_name="id", serializer=CourseSerializer):
        super().__init__(model, param_name, serializer)
        self.campus_mapping = {
    "JARAGUÁ RAU": "Instituto Federal de Santa Catarina - Campus Jaraguá do Sul - Rau",
}

    def get(self, request: HttpRequest, pk: str = None) -> Response:
        return super().get(request, pk, False)

    def post(self, request: HttpRequest) -> Response:
        if 'post' not in self.allowed_methods:
            return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        if not request.user.is_authenticated:
            return Response({"error": f"You must be logged in to post a/an {self.model.__name__}"}, status=status.HTTP_403_FORBIDDEN)
        
        # Check if the data is a list or a single dictionary
        if isinstance(request.data, list):
            items = request.data
        elif isinstance(request.data, dict):
            # If it's a single JSON object, wrap it in a list
            items = [request.data]
        else:
            return Response({"error": "Expected a list or a single item"}, status=status.HTTP_400_BAD_REQUEST)
        
        processed_data = set()

        for row in items:
            try:
                year_created = row.get('ano_ingresso')
                course = row.get('Curso')
                campus = row.get('campus')
                modality = row.get('modalidade')
                shift = row.get('turno')
                time_required = row.get('Tempo_min_Integralizacao_Curso')
                course_type = row.get('Tipo de Curso')

                if not all([year_created, course, campus, modality, shift, time_required, course_type]):
                    # Skip rows with missing fields
                    continue

                # Check if the row already exists in the processed data
                if (year_created, course, campus, modality, shift, time_required, course_type) not in processed_data:
                    processed_data.add((year_created, course, campus, modality, shift, time_required, course_type))
                    print(campus)
                    # Find the institute by campus name
                    if campus in self.campus_mapping:
                        campus = self.campus_mapping[campus]
                    campus_regex = r'\b{}\b'.format(re.escape(campus.lower()))

                    # Filter the Institute using the regular expression
                    institute = Institute.objects.filter(name__iregex=campus_regex).first()
                    
                    if institute is None:
                        return Response({'error': f"No institute found for campus '{campus}'"}, status=status.HTTP_404_NOT_FOUND)
                    
                    # Check if the course type is present
                    if not course_type:
                        course_type = self.get_type_from_name(course)
                        if not course_type:
                            return Response({"error": "Type could not be parsed"}, status=status.HTTP_400_BAD_REQUEST)
                        
                    # Create or update the object in the database
                    Course.objects.update_or_create(
                        year_created=year_created,
                        name=course,
                        institute=institute,
                        modality=modality,
                        shift=shift,
                        type=course_type,
                        time_required=time_required
                    )
            except Exception as e:
                return Response({'error': 'Error while processing row: {}'.format(str(e))}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': 'Data processed successfully!'}, status=status.HTTP_200_OK)



       # else:
        #     data = request.data 
        #     if data['type'] != None:
        #         return super().post(request)
        #     else:
        #         name = data['name']
        #         type_from_name = self.get_type_from_name(name)
        #         if type_from_name == None:
        #             return Response({"error": "Type could not be parsed"}, status=status.HTTP_403_FORBIDDEN)
        
        #         data['type'] = type_from_name
        #         request.data = data
        #         return super().post(request)


    def put(self, request: HttpRequest, pk: str = None) -> Response:
        data = request.data 
        if data['type'] != None:
            return super().put(request)
        else:
            name = data['name']
            type_from_name = self.get_type_from_name(name)
            if type_from_name == None:
                return Response({"error": "Type could not be parsed"}, status=status.HTTP_403_FORBIDDEN)
    
            data['type'] = type_from_name
            request.data = data
            return super().put(request)


    def delete(self, request: HttpRequest, pk: str = None) -> Response:
        return super().delete(request, pk)
    




































class CurrentUserView(APIView):

    def get(self, request: HttpRequest) -> Response:
        if request.user.is_authenticated:
            serializer = CurrentCustomUserSerializer(request.user)
            return Response({"user": serializer.data}, status=status.HTTP_200_OK)
        return Response({"user": None}, status=status.HTTP_404_NOT_FOUND)


class CustomUserView(BaseView):
    def __init__(self, model=CustomUser, param_name="id", serializer=CustomUserSerializer):
        super().__init__(model, param_name, serializer)

    def get(self, request: HttpRequest, id: int = None) -> Response:
        return super().get(request, id)

    def required_fields(self, request: HttpRequest) -> bool | str:
        if not request.data.get("first_name"):
            return "First Name field is required"
        # if not request.data.get("email"):
        #     return "Email field is required"
        return False

    def post(self, request: HttpRequest, allowed: bool = False, permission_type: str = None) -> Response:
        if 'post' not in self.allowed_methods:
            return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if not allowed and not self.is_allowed(request):
            return self.not_allowed_response(permission_type)

        elif not request.user.is_authenticated:
            return Response({"error": f"You must be logged in to post a/an{self.model.__name__}"}, status=status.HTTP_403_FORBIDDEN)
        
        
        is_bulk = isinstance(request.data, list)
        if is_bulk:
            instances = []
            errors = []
            for item in request.data:
                serializer = self.serializer(data=item)
                if serializer.is_valid():
                    instance = serializer.save()
                    instances.append(serializer.data)
                else:
                    errors.append(serializer.errors)
            if errors:
                return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
            return Response(instances, status=status.HTTP_201_CREATED)
        else:
            serializer = self.serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: HttpRequest, pk: str | int = None, allowed: bool = False, permission_type: str | None = None) -> Response:
        if 'put' not in self.allowed_methods:
            return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if not allowed and not self.is_allowed(request):
            return self.not_allowed_response(permission_type)

        elif not request.user.is_authenticated:
            return Response({"error": f"You must be logged in to edit a/an{self.model.__name__}"}, status=status.HTTP_403_FORBIDDEN)
        
        self.parse_csv_data_in_request(request)
        
        is_bulk = isinstance(request.data, list)
        if is_bulk:
            instances = []
            for item in request.data:
                obj = self.get_object(item.get(self.param_name), request)
                serializer = self.serializer(obj, data=item, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    instances.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(instances, status=status.HTTP_200_OK)
        else:
            obj = self.get_object(pk, request)
            serializer = self.serializer(obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: HttpRequest, pk: str | int = None, allowed: bool = False, permission_type: str | None = None) -> Response:
        if 'delete' not in self.allowed_methods:
            return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if not allowed and not self.is_allowed(request):
            return self.not_allowed_response(permission_type)

        elif not request.user.is_authenticated:
            return Response({"error": f"You must be logged in to delete a/an{self.model.__name__}"}, status=status.HTTP_403_FORBIDDEN)
        
        self.parse_csv_data_in_request(request)
        
        is_bulk = isinstance(request.data, list)
        if is_bulk:
            instances = []
            for item in request.data:
                obj = self.get_object(item.get(self.param_name), request)
                obj.delete()
                instances.append({"success": True})
            return Response(instances, status=status.HTTP_200_OK)
        else:
            obj = self.get_object(pk, request)
            obj.delete()
            return Response({"success": True}, status=status.HTTP_200_OK)
class CurrentUserView(APIView):

    def get(self, request: HttpRequest) -> Response:
        if request.user.is_authenticated:
            serializer = CurrentCustomUserSerializer(request.user)
            return Response({"user": serializer.data}, status=status.HTTP_200_OK)
        return Response({"user": None}, status=status.HTTP_404_NOT_FOUND)


class CustomUserView(BaseView):
    def __init__(self, model=CustomUser, param_name="id", serializer=CustomUserSerializer):
        super().__init__(model, param_name, serializer)

    def get(self, request: HttpRequest, id: int = None) -> Response:
        return super().get(request, id)

    def required_fields(self, request: HttpRequest) -> bool | str:
        if not request.data.get("first_name"):
            return "First Name field is required"
        # if not request.data.get("email"):
        #     return "Email field is required"
        return False

    def post(self, request: HttpRequest, allowed: bool = False, permission_type: str = None) -> Response:
        if 'post' not in self.allowed_methods:
            return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if not allowed and not self.is_allowed(request):
            return self.not_allowed_response(permission_type)

        elif not request.user.is_authenticated:
            return Response({"error": f"You must be logged in to post a/an{self.model.__name__}"}, status=status.HTTP_403_FORBIDDEN)
        
        self.parse_csv_data_in_request(request)
        
        is_bulk = isinstance(request.data, list)
        if is_bulk:
            instances = []
            errors = []
            for item in request.data:
                serializer = self.serializer(data=item)
                if serializer.is_valid():
                    instance = serializer.save()
                    instances.append(serializer.data)
                else:
                    errors.append(serializer.errors)
            if errors:
                return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
            return Response(instances, status=status.HTTP_201_CREATED)
        else:
            serializer = self.serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: HttpRequest, pk: str | int = None, allowed: bool = False, permission_type: str | None = None) -> Response:
        if 'put' not in self.allowed_methods:
            return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if not allowed and not self.is_allowed(request):
            return self.not_allowed_response(permission_type)

        elif not request.user.is_authenticated:
            return Response({"error": f"You must be logged in to edit a/an{self.model.__name__}"}, status=status.HTTP_403_FORBIDDEN)
        
        self.parse_csv_data_in_request(request)
        
        is_bulk = isinstance(request.data, list)
        if is_bulk:
            instances = []
            for item in request.data:
                obj = self.get_object(item.get(self.param_name), request)
                serializer = self.serializer(obj, data=item, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    instances.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(instances, status=status.HTTP_200_OK)
        else:
            obj = self.get_object(pk, request)
            serializer = self.serializer(obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: HttpRequest, pk: str | int = None, allowed: bool = False, permission_type: str | None = None) -> Response:
        if 'delete' not in self.allowed_methods:
            return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if not allowed and not self.is_allowed(request):
            return self.not_allowed_response(permission_type)

        elif not request.user.is_authenticated:
            return Response({"error": f"You must be logged in to delete a/an{self.model.__name__}"}, status=status.HTTP_403_FORBIDDEN)
        
        self.parse_csv_data_in_request(request)
        
        is_bulk = isinstance(request.data, list)
        if is_bulk:
            instances = []
            for item in request.data:
                obj = self.get_object(item.get(self.param_name), request)
                obj.delete()
                instances.append({"success": True})
            return Response(instances, status=status.HTTP_200_OK)
        else:
            obj = self.get_object(pk, request)
            obj.delete()
            return Response({"success": True}, status=status.HTTP_200_OK)
class CustomUserLogin(APIView):

    def post(self, request: HttpRequest) -> Response:
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            serializer = CurrentCustomUserSerializer(request.user)
            return Response({'user': serializer.data})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class CustomUserLogout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest) -> Response:
        logout(request)   # Isso encerrará a sessão do usuário
        return Response({"success": True}, status=status.HTTP_200_OK)


def process_csv(file_path):
    # Carregar o arquivo CSV em um DataFrame do pandas
    df = pd.read_csv(file_path)

    # Iterar sobre cada linha do DataFrame
    for index, row in df.iterrows():
        # Criar um dicionário para armazenar os dados do estudante
        student_data = {
            'name': row['nome'],
            'mother_name': None,  # Como não há campo de nome da mãe, deixamos como None
            'father_name': row['nome_pai'],  # Usamos o campo 'nome_pai' para 'father_name'
            'birth_date': row['mes_ano_nascimento'],
            # Adicione mais campos conforme necessário
        }

        # Criar o estudante no banco de dados
        student_view = StudentView()
        student_response = student_view.post(request=None, data=student_data)
        if student_response.status_code != 201:
            print(f"Erro ao adicionar estudante {row['nome']}: {student_response.json()}")

        # Verificar se o campus existe no banco de dados com base no nome fornecido
        campus_name = row['campus']
        try:
            campus = Institute.objects.get(name=campus_name)
        except Institute.DoesNotExist:
            print(f"Campus {campus_name} não encontrado. Ignorando este registro.")
            continue

        # Criar um dicionário para armazenar os dados do curso
        course_data = {
            'name': row['Curso'],
            'shift': row['turno'],
            'modality': row['modalidade'],
            'type': None,  # O tipo será definido posteriormente
            'campus': campus.id,  # Usamos o ID do campus encontrado
            # Adicione mais campos conforme necessário
        }

        # Verificar se o curso já existe no mesmo campus antes de criar um novo curso
        existing_course = Course.objects.filter(name=row['Curso'], campus=campus)
        if existing_course.exists():
            course_id = existing_course.first().id
            print(f"Curso {row['Curso']} já existe no campus {campus_name}.")
        else:
            # Criar o curso no banco de dados
            course_view = CourseView()
            course_response = course_view.post(request=None, data=course_data)
            if course_response.status_code != 201:
                print(f"Erro ao adicionar curso {row['Curso']}: {course_response.json()}")
                continue
            course_id = course_response.json()['id']

        # Definir o tipo do curso com base no nome do curso
        type_from_name = PreviousSchoolView.get_type_from_name(row['Curso'])
        if type_from_name is None:
            print(f"Tipo do curso não pôde ser identificado para {row['Curso']}")
            continue

        # Atualizar o tipo do curso e salvar no banco de dados
        course_data['type'] = type_from_name
        course_response = course_view.put(request=None, pk=course_id, data=course_data)
        if course_response.status_code != 200:
            print(f"Erro ao atualizar tipo do curso {row['Curso']}: {course_response.json()}")

        # Criar um dicionário para armazenar os dados do status
        status_data = {
            'status': row['Status'],
            'current_semester': row['semestre_ingresso'],
            # Adicione mais campos conforme necessário
        }

        # Criar o status no banco de dados
        status_view = StatusView()
        status_response = status_view.post(request=None, data=status_data)
        if status_response.status_code != 201:
            print(f"Erro ao adicionar status para {row['nome']}: {status_response.json()}")

        # Criar uma entrada para o estudante no curso e salvar no banco de dados
        student_course_data = {
            'name': row['Curso'],
            'admission_process': row['Cota'],
            'ingressed_semester': row['semestre_ingresso'],
            'course': course_id,
            'student': student_response.json()['id'],
            'status': status_response.json()['id'],  # Referenciar o status criado
            # Adicione mais campos conforme necessário
        }

        student_course_view = StudentCourseView()
        student_course_response = student_course_view.post(request=None, data=student_course_data)
        if student_course_response.status_code != 201:
            print(f"Erro ao adicionar estudante ao curso {row['Curso']}: {student_course_response.json()}")


