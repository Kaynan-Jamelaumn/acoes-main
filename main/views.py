from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpRequest
from django.db.models import Q
from .serializers import CustomUserSerializer, CustomUserListSerializer, CurrentCustomUserSerializer, CitySerializer, AddressSerializer, InstituteSerializer, PreviousSchoolSerializer, CourseSerializer, StatusSerializer, StudentSerializer, StudentCourseSerializer
from .models import CustomUser, City, Address, Institute, PreviousSchool, Course, Student, StudentCourse, Status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password

from .models import CustomUser
from BaseView import BaseView

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

    def get(self, request: HttpRequest, pk: str = None) -> Response:
        return super().get(request, pk, False)

    def post(self, request: HttpRequest) -> Response:
        data = request.data 
        if data['type'] != None:
            return super().post(request)
        else:
            name = data['name']
            type_from_name = self.get_type_from_name(name)
            if type_from_name == None:
                return Response({"error": "Type could not be parsed"}, status=status.HTTP_403_FORBIDDEN)
    
            data['type'] = type_from_name
            request.data = data
            return super().post(request)


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


class StudentView(BaseView):
    def __init__(self, model=Student, param_name="id", serializer=StudentSerializer):
        super().__init__(model, param_name, serializer)

    def get(self, request: HttpRequest, pk: str = None) -> Response:
        return super().get(request, pk, False)
        

    def post(self, request: HttpRequest) -> Response:
        return super().post(request)

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
