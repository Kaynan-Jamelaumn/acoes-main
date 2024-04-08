from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Model
from django.http import HttpRequest
from rest_framework.serializers import Serializer
import csv
import json
from rest_framework.parsers import JSONParser
from rest_framework.pagination import PageNumberPagination

from rest_framework.parsers import BaseParser
class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # Set the number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 50
class CSVParser(BaseParser):
    """
    Parses CSV serialized data.
    """

    media_type = 'text/csv'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Parses the incoming bytestream as CSV and returns the resulting data.
        """
        # Decode the stream as a string
        stream_string = stream.read().decode('utf-8')
        # Pass the decoded string to csv.DictReader
        reader = csv.DictReader(stream_string.splitlines())
        return list(reader)  # Convert CSV data into a list of dictionaries



class BaseView(APIView):
    parser_classes = (CSVParser, JSONParser)
    pagination_class = CustomPageNumberPagination 
    def __init__(self, model: Model, param_name: str, serializer: Serializer,  allowed_methods : list[str] = ['get', 'post', 'put', 'delete']):
        self.__model = model
        self.__param_name = param_name
        self.__serializer = serializer
        self.__allowed_methods = allowed_methods


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

    @property
    def allowed_methods(self) -> list[str]:
        return self.__allowed_methods

    @allowed_methods.setter
    def allowed_methods(self, value: list[str]):
        self.__allowed_methods = value

    def is_allowed(self, request: HttpRequest):
        return request.user.is_staff

    def not_allowed_response(self, permission_type: str | None = None):
        if permission_type:
            return Response({f"error": "You do not have the necessary permission to {permission_type} an/a {self.model}"}, status=status.HTTP_403_FORBIDDEN)
        return Response({"error": "You do not have the necessary permissions"}, status=status.HTTP_403_FORBIDDEN)

    def check_obj(self, obj):
        if not obj:
            return Response({"error": f"{self.model.__name__} not found"}, status=status.HTTP_404_NOT_FOUND)

    def to_retrieve(self, request: HttpRequest = None, pk: str | int = None, many: bool = False, page: int = False):

        if pk != None:
            if many == True:
                obj = self.get_object(request, pk=pk, many=True)
                self.check_obj(obj)
                serializer = self.serializer(obj,  many=True)
            else:
                obj = self.get_object(request, pk)
                self.check_obj(obj)
                serializer = self.serializer(obj)
        elif request.data.get(self.param_name) and page == 0:
            if many == True:
                obj = self.get_object(request, many=True)
                self.check_obj(obj)
                serializer = self.__serializer(obj, many=True)
            else:
                obj = self.get_object(request)
                self.check_obj(obj)
                serializer = self.__serializer(obj)

        else:
            # Pagination of all objects if no specific filter or primary key provided
            serializer = self.__serializer(
            data=self.model.objects.all(), many=True)
            serializer.is_valid()
        return serializer

    def get_object(self, request: HttpRequest = None, pk: str | int = None, many: bool = False):
        if many:
            if isinstance(pk, list):
                # Handle a list of primary keys for bulk operations
                return self.model.objects.filter(**{f'{self.param_name}__in': pk})
            elif isinstance(request.data, list):
                # Handle a list of dictionaries with primary keys
                pks = [item[self.param_name] for item in request.data]
                return self.model.objects.filter(**{f'{self.param_name}__in': pks})
            else:
                # Handle a single dictionary
                value = request.data.get(self.param_name)
                if value is not None:
                    return self.model.objects.filter(**{self.param_name: value})
                else:
                    raise ValueError("No valid identifier provided for bulk operation")
        else:
            if pk !=None:
                return self.model.objects.get(**{self.param_name: pk})
            else:
                value = request.data.get(self.param_name)
                if value is not None:
                    return self.model.objects.get(**{self.param_name: value})
                else:
                    raise ValueError(f"{self.model.name} not found")
    def get(self, request: HttpRequest, pk: str | int = None, allowed: bool = True, permission_type: str = None, page: int = 0) -> Response:
        if 'get' not in self.allowed_methods:
            return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if not allowed and not self.is_allowed(request): # eu n lembro o q siginificava isso aqui é se allowed == false ?
            return self.not_allowed_response(permission_type)
        else:
            print(page)
            #page = request.query_params.get('page', 0)
            if page !=0:  # If page parameter is provided
                queryset = self.model.objects.all()
                paginator = self.pagination_class()
                paginated_queryset = paginator.paginate_queryset(queryset, request)
                serializer = self.serializer(paginated_queryset, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                serializer = self.to_retrieve(request=request, pk=pk, page=page)
                return Response(serializer.data, status=status.HTTP_200_OK)
            # serializer = self.to_retrieve(request=request, pk=pk, page=page)
            # return Response(serializer.data,  status=status.HTTP_200_OK)

    def post(self, request: HttpRequest, allowed: bool = False, permission_type: str = None) -> Response:
        if 'post' not in self.allowed_methods:
            return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if not allowed and not self.is_allowed(request):
            return self.not_allowed_response(permission_type)

        elif not request.user.is_authenticated:
            return Response({"error": f"You must be logged in to post a/an{self.model.__name__}"}, status=status.HTTP_403_FORBIDDEN)
        
        is_bulk = isinstance(request.data, list)

        serializer = self.serializer(data=request.data, many=is_bulk)
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
            return Response({"error": f"You must be logged in to edit a/an {self.model.__name__}"}, status=status.HTTP_403_FORBIDDEN)
        
        is_bulk = isinstance(request.data, list)

        if is_bulk:
            # Iterate over each item in the request data
            for item in request.data:
                # Check if 'pk' field exists in the item
                if self.__param_name not in item:
                    return Response({"error": "'pk' field is required for bulk update"}, status=status.HTTP_400_BAD_REQUEST)
                
                try:
                    # Get the object using 'pk' and update it
                    obj = self.get_object(request=request, pk=item[self.__param_name])
                    serializer = self.serializer(obj, data=item, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except self.model.DoesNotExist:
                    return Response({"error": f"{self.model.__name__} with id {item[self.__param_name]} does not exist"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"sucess": serializer.data}, status=status.HTTP_200_OK)
        else:
            # If it's a single update, proceed as before
            try:
                obj = self.get_object(request=request, pk=pk)
                serializer = self.serializer(obj, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except self.model.DoesNotExist:
                return Response({"error": f"{self.model.__name__} with id {pk} does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request: HttpRequest, pk: str | int = None, allowed: bool = False, permission_type: str | None = None) -> Response:
        if 'delete' not in self.allowed_methods:
            return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if not allowed and not self.is_allowed(request):
            return self.not_allowed_response(permission_type)

        elif not request.user.is_authenticated:
            return Response({"error": f"You must be logged in to delete a/an{self.model.__name__}"}, status=status.HTTP_403_FORBIDDEN)
        
        is_bulk = isinstance(request.data, list)
        objs = self.get_object(request=request, pk=pk, many=is_bulk)
        
        if isinstance(objs, Response):
            return objs
   
        if not objs:
            return Response({"error": "one or more object could not be found" }, status=status.HTTP_400_BAD_REQUEST)
        if is_bulk:
            for obj in objs:
                obj.delete()
            return Response({"success": "Bulk delete operation completed."}, status=status.HTTP_202_ACCEPTED)
        else:
            objs.delete()
            return Response({"success": "Delete operation completed."}, status=status.HTTP_202_ACCEPTED)





#new bulk



def post(self, request: HttpRequest) -> Response:
    if 'post' not in self.allowed_methods:
        return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    if not self.is_allowed(request):
        return self.not_allowed_response("create")

    elif not request.user.is_authenticated:
        return Response({"error": f"You must be logged in to post a/an{self.model.__name__}"}, status=status.HTTP_403_FORBIDDEN)
    
    is_bulk = isinstance(request.data, list)

    if is_bulk:
        success_data = []
        error_data = []
        for item in request.data:
            serializer = self.serializer(data=item)
            if serializer.is_valid():
                serializer.save()
                success_data.append(serializer.data)
            else:
                error_data.append(serializer.errors)
        if error_data:
            return Response({"success": success_data, "errors": error_data}, status=status.HTTP_206_PARTIAL_CONTENT)
        else:
            return Response({"success": success_data}, status=status.HTTP_201_CREATED)
    else:
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def put(self, request: HttpRequest, pk: str | None = None) -> Response:
    if 'put' not in self.allowed_methods:
        return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    if not self.is_allowed(request):
        return self.not_allowed_response("edit")

    elif not request.user.is_authenticated:
        return Response({"error": f"You must be logged in to edit a/an {self.model.__name__}"}, status=status.HTTP_403_FORBIDDEN)
    
    is_bulk = isinstance(request.data, list)

    if is_bulk:
        success_data = []
        error_data = []
        for item in request.data:
            if self.__param_name not in item:
                error_data.append({"error": "'pk' field is required for bulk update"})
                continue
            try:
                obj = self.get_object(request=request, pk=item[self.__param_name])
                serializer = self.serializer(obj, data=item, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    success_data.append(serializer.data)
                else:
                    error_data.append(serializer.errors)
            except self.model.DoesNotExist:
                error_data.append({"error": f"{self.model.__name__} with id {item[self.__param_name]} does not exist"})
        if error_data:
            return Response({"success": success_data, "errors": error_data}, status=status.HTTP_206_PARTIAL_CONTENT)
        else:
            return Response({"success": success_data}, status=status.HTTP_200_OK)
    else:
        try:
            obj = self.get_object(request=request, pk=pk)
            serializer = self.serializer(obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except self.model.DoesNotExist:
            return Response({"error": f"{self.model.__name__} with id {pk} does not exist"}, status=status.HTTP_404_NOT_FOUND)

def delete(self, request: HttpRequest, pk: str | int = None) -> Response:
    if 'delete' not in self.allowed_methods:
        return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    if not self.is_allowed(request):
        return self.not_allowed_response("delete")

    elif not request.user.is_authenticated:
        return Response({"error": f"You must be logged in to delete a/an{self.model.__name__}"}, status=status.HTTP_403_FORBIDDEN)
    
    is_bulk = isinstance(request.data, list)
    objs = self.get_object(request=request, pk=pk, many=is_bulk)
    
    if isinstance(objs, Response):
        return objs
   
    if not objs:
        return Response({"error": "one or more objects could not be found" }, status=status.HTTP_400_BAD_REQUEST)
    if is_bulk:
        success_data = []
        error_data = []
        for obj in objs:
            obj.delete()
            success_data.append({"success": f"Deleted {self.model.__name__} with id {obj.pk}"})
        if error_data:
            return Response({"success": success_data, "errors": error_data}, status=status.HTTP_206_PARTIAL_CONTENT)
        else:
            return Response({"success": success_data}, status=status.HTTP_202_ACCEPTED)
    else:
        objs.delete()
        return Response({"success": f"Deleted {self.model.__name__} with id {pk}"}, status=status.HTTP_202_ACCEPTED)