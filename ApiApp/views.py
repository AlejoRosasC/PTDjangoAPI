from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
import json

from ApiApp.models import Peticion
from ApiApp.serializers import PeticionSerializer

# Create your views here.

@csrf_exempt
def peticionApi(request,id=0):
    #Metodo GET / muestra todos los registros
    if request.method =='GET':
        peticion = Peticion.objects.all()
        peticion_srlzr = PeticionSerializer(peticion, many=True)
        response_data = json.dumps(peticion_srlzr.data)#linea nueva
        print(f"Los valores son: {response_data}")
        return JsonResponse(response_data, safe=False, content_type="application/json") #linea nueva
        
        #return JsonResponse(peticion_srlzr.data,safe=False)
    

    #Metodo POST / Crea un nuevo registro 
    elif request.method == 'POST':
        peticion_data = JSONParser().parse(request)
        peticion_srlzr = PeticionSerializer(data = peticion_data)
        if peticion_srlzr.is_valid():
            peticion_srlzr.save()
            return JsonResponse("Added Succesfully", safe = False)
        return JsonResponse("Failed to Add", safe = False)
    
    #Metodo PUT / Edita un registro existente 
    elif request.method == 'PUT':
        peticion_data = JSONParser().parse(request)
        peticion = Peticion.objects.get(PeticionId=peticion_data['PeticionId'])
        peticion_srlzr = PeticionSerializer(peticion, data = peticion_data)
        if peticion_srlzr.is_valid():
            peticion_srlzr.save()
            return JsonResponse("Updated Succesfully", safe = False)
        return JsonResponse("Failed to update", safe = False)
    
    #Metodo DELETE / elimina un registro existente
    elif request.method == 'DELETE':
        peticion = Peticion.objects.get(PeticionId=id)
        peticion.delete()
        return JsonResponse("Deleted Succesfully", safe=False)


    
