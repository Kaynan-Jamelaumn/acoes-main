from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Model
from django.http import HttpRequest
from django.db.models import Q
from rest_framework.serializers import Serializer
from .serializers import CustomUserSerializer, CustomUserListSerializer, CurrentCustomUserSerializer, CitySerializer, AddressSerializer, InstituteSerializer, PreviousSchoolSerializer, CourseSerializer, StatusSerializer, StudentSerializer, StudentCourseSerializer
from .models import CustomUser, City, Address, Institute, PreviousSchool, Course, Student, StudentCourse, Status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password

from .models import CustomUser


class BaseView(APIView):

    def __init__(self, model: Model, param_name: str, serializer: Serializer):
        self.__model = model
        self.__param_name = param_name
        self.__serializer = serializer

    @property
    def model(self) -> Model:
        return self.__model

    @model.setter
    def model(self, value: Model):
        self.__model = value

    @property
    def param_name(self) -> str:
        return self.__param_name

    @param_name.setter
    def param_name(self, value: str):
        self.__param_name = value

    @property
    def serializer(self) -> Serializer:
        return self.__serializer

    @serializer.setter
    def serializer(self, value: Serializer):
        self.__serializer = value

    def is_allowed(self, request: HttpRequest):
        return request.user.is_staff

    def not_allowed_response(self, permission_type: str | None = None):
        if permission_type:
            return Response({f"error": "You do not have the necessary permission to {permission_type} an/a {self.model}"}, status=status.HTTP_403_FORBIDDEN)
        return Response({"error": "You do not have the necessary permissions"}, status=status.HTTP_403_FORBIDDEN)

    def check_obj(self, obj):
        if not obj:
            return Response({"error": f"{self.model.__name__} not found"}, status=status.HTTP_404_NOT_FOUND)

    def to_retrieve(self, request: Model = None, pk: str | int = None, many: bool = False):

        if pk:
            if many == True:
                obj = self.get_object(pk=pk, many=True)
                self.check_obj(obj)
                serializer = self.serializer(obj,  many=True)
            else:
                obj = self.get_object(pk)
                self.check_obj(obj)
                serializer = self.serializer(obj)
        elif request.data.get(self.param_name):
            if many == True:
                obj = self.get_object(request, many=True)
                self.check_obj(obj)
                serializer = self.__serializer(obj, many=True)
            else:
                obj = self.get_object(request)
                self.check_obj(obj)
                serializer = self.__serializer(obj)

        else:
            serializer = self.__serializer(
                data=self.model.objects.all(), many=True)
            serializer.is_valid()
        return serializer

    def get_object(self, pk: str | int, request: HttpRequest = None, many: bool = False):
        if many == True:
            if pk:
                # Retorna o primeiro objeto correspondente.__param_name: pk})
                obj = self.model.objects.filter(**{self.__param_name: pk})
            else:
                obj = self.model.objects.filter(
                    **{self.__param_name: request.data.get(self.__param_name)})
        else:
            if pk:
                # Retorna o primeiro objeto correspondente.__param_name: pk})
                obj = self.model.objects.get(**{self.__param_name: pk})
            else:
                obj = self.model.objects.get(
                    **{self.__param_name: request.data.get(self.__param_name)})
        if obj:
            return obj
        return Response({"error": f"{self.model.__name__} not found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request: HttpRequest, pk: str | int = None, allowed: bool = True, permission_type: str = None) -> Response:
         if not allowed and not self.is_allowed(request): # eu n lembro o q siginificava isso aqui é se allowed == false ?
            return self.not_allowed_response(permission_type)
         else:
            serializer = self.to_retrieve(request, pk)
            return Response(serializer.data,  status=status.HTTP_200_OK)

    def post(self, request: HttpRequest, allowed: bool = False, permission_type: str = None) -> Response:
        if not allowed and not self.is_allowed(request):
            return self.not_allowed_response(permission_type)

        elif not request.user.is_authenticated:
            return Response({"error": f"You must be logged in to post a/an{self.model.__name__}"}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: HttpRequest, pk: str | int = None, allowed: bool = False, permission_type: str | None = None) -> Response:
        if not allowed and not self.is_allowed(request):
            return self.not_allowed_response(permission_type)

        elif not request.user.is_authenticated:
            return Response({"error": f"You must be logged in to edit a/an{self.model.__name__}"}, status=status.HTTP_403_FORBIDDEN)
        obj = self.get_object(pk, request)
        serializer = self.serializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: HttpRequest, pk: str | int = None, allowed: bool = False, permission_type: str | None = None) -> Response:
        if not allowed and not self.is_allowed(request):
            return self.not_allowed_response(permission_type)

        elif not request.user.is_authenticated:
            return Response({"error": f"You must be logged in to delete a/an{self.model.__name__}"}, status=status.HTTP_403_FORBIDDEN)
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

    def post(self, request: HttpRequest) -> Response:
        message = self.required_fields(request)
        if message:
            return Response({"detail": "Email field is required"}, status=status.HTTP_400_BAD_REQUEST)
        request.data['password'] = make_password(request.data['password'])

        serializer = CustomUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        login(request, user)

        return Response({"user": serializer.data}, status=status.HTTP_201_CREATED)

    def put(self, request: HttpRequest, id: id = None) -> Response:
        user = self.to_retrieve(request, id)

        if isinstance(user, self.serializer):  # Check if user is a serializer
            user_instance = user.instance  # Extract the model instance from the serializer
        else:
            user_instance = user

        if request.user != user_instance and not request.user.is_staff:
            return Response({"error": "You do not have permission to edit this user"}, status=status.HTTP_403_FORBIDDEN)

        if 'password' in request.data:
            request.data['password'] = make_password(request.data['password'])

        serializer = self.serializer(
            user_instance, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request: HttpRequest, id: id = None) -> Response:
        user = self.to_retrieve(request, id)

        if isinstance(user, self.serializer):  # Check if user is a serializer
            user_instance = user.instance  # Extract the model instance from the serializer
        else:
            user_instance = user
        if request.user != user and not request.user.is_staff:
            return Response({"error": "You do not have permission to delete this user"}, status=status.HTTP_403_FORBIDDEN)
        user_instance.is_active = False
        user_instance.save()
        return Response({"error": "User deleted successfully"}, status=status.HTTP_200_OK)


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
        return super().get(request, pk)

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
        return super().get(request, pk)

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
        return super().get(request, pk)

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
        return super().get(request, pk)

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
        return super().get(request, pk)

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
        return super().get(request, pk)

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
        return super().get(request, pk)

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
            'studant': studants_serializer.data,
        }
        return Response(serialized_data, status=status.HTTP_200_OK)


class StudentsBySex(APIView):

    def get(self, request: HttpRequest, sex: str = None) -> Response:
        if not sex:
            sex = request.data.get('sex')

        object = Student.objects.filter(sex=sex)
        if object:
            serializer = StudentSerializer(object, many=True)
            return Response({"students": serializer.data}, status=status.HTTP_200_OK)
        return Response({"students": None}, status=status.HTTP_200_OK)

class StudentsByGender(APIView):

    def get(self, request: HttpRequest, gender: str = None) -> Response:
        if not gender:
            gender = request.data.get('gender')

        object = Student.objects.filter(gender=gender)
        if object:
            serializer = StudentSerializer(object, many=True)
            return Response({"students": serializer.data}, status=status.HTTP_200_OK)
        return Response({"students": None}, status=status.HTTP_200_OK)

class StudentsByColor_Race(APIView):

    def get(self, request: HttpRequest, color_race: str = None) -> Response:
        if not color_race:
            color_race = request.data.get('color_race')

        object = Student.objects.filter(color_race=color_race)
        if object:
            serializer = StudentSerializer(object, many=True)
            return Response({"students": serializer.data}, status=status.HTTP_200_OK)
        return Response({"students": None}, status=status.HTTP_200_OK)

class StudentsByDisability(APIView):

    def get(self, request: HttpRequest, disability: str = None) -> Response:
        if not disability:
            disability = request.data.get('disability')

        object = Student.objects.filter(disability=disability)
        if object:
            serializer = StudentSerializer(object, many=True)
            return Response({"students": serializer.data}, status=status.HTTP_200_OK)
        return Response({"students": None}, status=status.HTTP_200_OK)




class StudentsByMother(APIView):

    def get(self, request: HttpRequest, mother_name: str = None) -> Response:
        if not mother_name:
            mother_name = request.data.get('mother_name')

        object = Student.objects.filter(mother_name__icontains=mother_name)
        if object:
            serializer = StudentSerializer(object, many=True)
            return Response({"students": serializer.data}, status=status.HTTP_200_OK)
        return Response({"students": None}, status=status.HTTP_200_OK)


class StudentsByFather(APIView):

    def get(self, request: HttpRequest, father_name: str = None) -> Response:
        if not father_name:
            father_name = request.data.get('father_name')

        object = Student.objects.filter(father_name__icontains=father_name)
        if object:
            serializer = StudentSerializer(object, many=True)
            return Response({"students": serializer.data}, status=status.HTTP_200_OK)
        return Response({"students": None}, status=status.HTTP_200_OK)


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


# class StudentsByInstituteAndShift(APIView):

#     def get(self, request: HttpRequest, institute: str = None, id: int = None) -> Response:
#         if not id:
#             id = request.data.get('id')
#         if not institute:
#             institute = request.data.get('institute')
#         object = Student.objects.filter(id=id, institute=institute)
#         if object:
#             serializer = StudentCourseSerializer(object, many=True)
#             return Response({"students": serializer.data}, status=status.HTTP_200_OK)
#         return Response({"students": None}, status=status.HTTP_200_OK)
