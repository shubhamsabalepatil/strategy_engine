from django.shortcuts import render
from rest_framework.views import APIView
from .models import Strategy,Parameter,Instance,Strategy_type, Time_frame
from .serializers import Strategy_serializer,Parameter_serializer,Instance_serializer, Strategy_type_serializer, Time_frame_serializer
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse, HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view
import logging
from pymongo import MongoClient



# Create your views here.
class Strategy_api(APIView):
    def get(self,r, pk= None):
        code = pk
        try:
            if code is not None:
                get_strategy_by_code = Strategy.objects.get(code = code)
                serializer = Strategy_serializer(get_strategy_by_code)
                return Response(serializer.data, status= status.HTTP_200_OK)
            get_all_strategy = Strategy.objects.all()
            serializer_of_all_strategy = Strategy_serializer(get_all_strategy, many=True)
            return Response(serializer_of_all_strategy.data, status=status.HTTP_200_OK)
        except Exception:
            response = JsonResponse({'msg':'Startegy Not Found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self,r):
        try:
            serializer = Strategy_serializer(data= r.data)
            if serializer.is_valid():
                serializer.save()
                return Response('New Strategy Created',status=status.HTTP_201_CREATED)
            json_data = JSONRenderer().render(serializer.errors)
            return HttpResponse(json_data,content_type='application/json')
        except:
            response = JsonResponse({'msg': "Invalid Details-Cant Create Strategy"},status=status.HTTP_400_BAD_REQUEST)
            return response



    def put(self, r, pk=None, format = None):
        UNIV_ID = pk
        try:
            update_strategy = Strategy.objects.get(pk = UNIV_ID)
            serializer = Strategy_serializer(update_strategy,data=r.data, partial=True)
            #print(serializer)
            print(r.data)
            print(serializer.is_valid())
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'Strategy Updated'}, status=status.HTTP_201_CREATED)
        except Exception:
            response = JsonResponse({'msg': 'Invalid Details Cant Update Strategy'}, status=status.HTTP_400_BAD_REQUEST)
            return response

    def delete(self,r,pk=None):
        code = pk
        try:
            delete_strategy = Strategy.objects.get(pk=code)
            if delete_strategy.delete():
                return Response({'msg':'Strategy Deleted'},status=status.HTTP_204_NO_CONTENT)
        except Exception:
            response =JsonResponse({'msg':'Strategy doesnt exist'},status=status.HTTP_404_NOT_FOUND)
            return response

    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated]


class Parameter_api(APIView):
    def get(self,r,pk=None):
        variable = pk
        try:
            if variable is not None:
                get_parameter_by_id = Parameter.objects.get(variable = variable)
                serializer = Parameter_serializer(get_parameter_by_id)
                return Response(serializer.data,status=status.HTTP_200_OK)
            get_all_parameters = Parameter.objects.all()
            serializer_of_all_parameter = Parameter_serializer(get_all_parameters, many=True)
            return Response(serializer_of_all_parameter.data, status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({'msg':'Parameter Not Found'},status=status.HTTP_404_NOT_FOUND)

    def post(self,r):
        try:
            serializer =Parameter_serializer(data=r.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'New Parameter Created'}, status=status.HTTP_201_CREATED)
            json_data = JSONRenderer.render(serializer.errors)
            return HttpResponse(json_data,content='application/json')
        except:
            return JsonResponse({'msg':'Invalid Details CAnt Create Parameter'},status=status.HTTP_404_NOT_FOUND)

    def put(self,r,pk=None,format = None):
        variable = pk
        try:
            update_parameter = Parameter.objects.get(variable=variable)
            serializer = Parameter_serializer(update_parameter, data=r.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Parameter Updated'}, status=status.HTTP_201_CREATED)
        except Exception:
            response = JsonResponse({'msg': 'Invalid Details Cant Update Parameter'}, status=status.HTTP_400_BAD_REQUEST)
            return response


    def delete(self,r,pk=None):
        variable =pk
        print('hii')
        try:
            delete_parameter = Parameter.objects.get(variable=variable)
            if delete_parameter.delete():
                return Response({'msg':'Parameter Deleted'},status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return JsonResponse({'msg':'Parameter Not Found'},status=status.HTTP_404_NOT_FOUND)

    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated]

class Instance_api(APIView):
    def get(self,r,pk=None):
        name = pk
        try:
            if name is not None:
                get_parameter_by_id = Instance.objects.get(name = name)
                serializer = Instance_serializer(get_parameter_by_id)
                return Response(serializer.data,status=status.HTTP_200_OK)
            get_all_instance = Instance.objects.all()
            serializer_of_all_instance = Instance_serializer(get_all_instance, many=True)
            return Response(serializer_of_all_instance.data, status=status.HTTP_200_OK)
        except Exception:
            return JsonResponse({'msg':'Instance Not Found'},status=status.HTTP_404_NOT_FOUND)

    def post(self,r):
        try:
            serializer = Instance_serializer(data=r.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'New Instance Created'}, status=status.HTTP_201_CREATED)
            json_data = JSONRenderer.render(serializer.errors)
            return HttpResponse(json_data, content='application/json')
        except Exception as e:
            return JsonResponse({'msg':e})

    def put(self,r,pk=None):
        name =pk
        try:
            update_instance = Instance.objects.get(name =name)
            serializer = Instance_serializer(update_instance,data=r.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'Instance Updated'},status=status.HTTP_201_CREATED)
        except Exception:
            return JsonResponse({'msg':'Invalid Details Cant Update Instance'})

    def delete(self,r,pk=None):
        name =pk
        try:
            delete_instance= Instance.objects.get(name=name)
            if delete_instance.delete():
                return Response({'msg':'Instance Deleted'},status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return JsonResponse({'msg':'Instance Not Found'},status=status.HTTP_404_NOT_FOUND)

    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated]

class Strategy_type_api(APIView):
    def post(self,r):
        try:
            serializer = Strategy_type_serializer(data=r.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'New Strategy Type Created'}, status=status.HTTP_201_CREATED)
            json_data = JSONRenderer.render(serializer.errors)
            return HttpResponse(json_data, content='application/json')
        except:
            return JsonResponse({'msg':'Invalid Details Cant Create Strategy Type'})

    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated]

class Time_frame_api(APIView):
    def post(self,r):
        try:
            serializer = Time_frame_serializer(data=r.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'New Time Frame Created'}, status=status.HTTP_201_CREATED)
            json_data = JSONRenderer.render(serializer.errors)
            return HttpResponse(json_data, content='application/json')
        except:
            return JsonResponse({'msg': 'Invalid Details Cant Create Strategy Type'})

    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated]

@api_view(['GET'])
def get_strategy(r):
    getstrategy = Strategy.objects.all()
    serializer = Strategy_serializer(getstrategy,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def post_instance(r):
    serializer = Instance_serializer(data=r.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'msg': 'created'})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def get_parameter(r):
    getstrategy = Parameter.objects.all()
    serializer = Parameter_serializer(getstrategy,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_instance(r):
    getinstance = Instance.objects.all()
    serializer = Instance_serializer(getinstance,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


logger = logging.getLogger(__name__)

def hello_reader(r):
    logger = logging.getLogger(__name__)
    user = r.user if r.user.is_authenticated else 'AnonymousUser'
    method = r.method
    path = r.path
    logger.info(f'{user} made a {method} request to {path}')
    return HttpResponse("<h1>Hello FreeCodeCamp.org Reader :)</h1>")

from rest_framework import generics


class InstanceCreateView(generics.CreateAPIView):
    queryset = Instance.objects.all()
    serializer_class = Instance_serializer

class Strategy_create_view(generics.CreateAPIView):
    qs = Strategy.objects.all()
    sc = Strategy_serializer



def get_additional_fields(collection_name):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['strategy_engine2']
    collection = db[collection_name]
    query = {} # your query goes here
    projection = {field: 1 for field in collection.find_one().keys()} # include all fields
    rows = collection.find(query, projection)
    results = []
    for row in rows:
        row['_id'] = str(row['_id']) # convert ObjectId to string
        results.append(row)
    return results

@api_view(['GET'])
def get_instance_parameter(r):
    additional_fields = get_additional_fields('instance_instance')
    return Response(additional_fields)



def create_document(collection_name, document):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['strategy_engine2']
    collection = db[collection_name]
    result = collection.insert_one(document)
    return str(result.inserted_id)

@api_view(['POST'])
def post_instance_parameter(request):
    data = request.data
    result = create_document('instance_instance', data)
    return Response({'message': 'Document created', 'id': result})


def update_document(collection_name, name, update):
    print('hii1')
    client = MongoClient('mongodb://localhost:27017/')
    db = client['strategy_engine2']
    collection = db[collection_name]
    result = collection.update_one({'name': name}, {'$set': update})
    return result.modified_count > 0

@api_view(['PUT'])
def put_instance_parameter(request, name):
    print('hii')
    data = request.data
    print('data',data)
    result = update_document('instance_instance', name, data)
    if result:
        return Response({'message': 'Document updated'})
    else:
        return Response({'message': 'Document not found'})




def delete_document(collection_name, document_id):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['my_database']
    collection = db[collection_name]
    result = collection.delete_one


