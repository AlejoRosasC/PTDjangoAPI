from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

import json
from django.http import HttpResponse

from RestApiApp.models import Peticion
from RestApiApp.serializers import PeticionSerializer

import requests
from datetime import datetime

# Create your views here.

@csrf_exempt
def peticionApi(request,id=0):
    #Metodo GET / muestra todos los registros
    if request.method =='GET':

        peticion = Peticion.objects.all()
        #peticion_srlzr = PeticionSerializer(peticion, many=True)
        
        listResponse = []
        dictResponse = {}

        for i in peticion:
            dictResponse["PeticionId"] = i.PeticionId
            dictResponse["PeticionDate"] = str(i.PeticionDate)
            dictResponse["PeticionMethod"] = i.PeticionMethod
            dictResponse["PeticionConsult"] = i.PeticionConsult
            dictResponse["PeticionDataReturn"] = i.PeticionDataReturn

            listResponse.append(dictResponse.copy())

        response = json.dumps(listResponse)

        return HttpResponse(response,content_type='application/json')
    
    #Metodo PUT / Edita un registro existente 
    if request.method == 'PUT':
        peticion_data = JSONParser().parse(request)
        print(f"Valores: {peticion_data}")
        peticion = Peticion.objects.get(PeticionId=peticion_data['PeticionId'])
        peticion_srlzr = PeticionSerializer(request, data=peticion_data)
        print(peticion_srlzr)
        if peticion_srlzr.is_valid():
            
            peticion.PeticionDate = str(peticion_data['PeticionDate']),
            peticion.PeticionMethod = peticion_data['PeticionMethod'],
            peticion.PeticionConsult = peticion_data['PeticionConsult'],
            peticion.PeticionDataReturn = peticion_data['PeticionDataReturn']
            

            peticion.save()

            return JsonResponse("Registro Modificado", safe=False)
    
    #Metodo DELETE / elimina un registro existente
    elif request.method == 'DELETE':
        peticion = Peticion.objects.get(PeticionId=id)
        peticion.delete()
        return JsonResponse("Deleted Succesfully", safe=False)

@csrf_exempt
def mostrarUsuarios(request):
    if request.method == 'GET':
        method = "GET"
        endpoint = "https://jsonplaceholder.typicode.com/users"
        timestamp = datetime.now()

        response = requests.get(endpoint)
        response_data = response.json()

        info = Peticion(
            PeticionDate=timestamp.date(),
            PeticionMethod=method,
            PeticionConsult=endpoint,
            PeticionDataReturn=response_data
        )
        info.save()

        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
@csrf_exempt
def mostrarPublicaciones(request):
    if request.method == 'GET':
        method = "GET"
        endpoint = "https://jsonplaceholder.typicode.com/posts"
        timestamp = datetime.now()

        response = requests.get(endpoint)
        response_data = response.json()

        info = Peticion(
            PeticionDate=timestamp.date(),
            PeticionMethod=method,
            PeticionConsult=endpoint,
            PeticionDataReturn=response_data
        )


        info.save()

        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def fotosPorUsuario(request, id=0):
    if request.method == 'GET':
        method = "GET"
        endpoint_1 = f"https://jsonplaceholder.typicode.com/albums?userId={id}"
        endpoint_2 = "https://jsonplaceholder.typicode.com/photos?albumId="
        timestamp = datetime.now()

        response_1 = requests.get(endpoint_1)
        response_data_1 = response_1.json()

        list_1 = []
        list_2 = []

        for obj in response_data_1:
            if obj["userId"] == int(id):
                list_1.append(obj["id"])

        for id_ in list_1:
            url = endpoint_2 + str(id_)
            response_2 = requests.get(url)
            response_data_2 = response_2.json()
            list_2.extend(response_data_2)

        json_data = list_2

        info = Peticion(
            PeticionDate=timestamp.date(),
            PeticionMethod=method,
            PeticionConsult=endpoint_2,
            PeticionDataReturn=json_data
        )
        info.save()

        return JsonResponse(json_data, safe=False)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)
