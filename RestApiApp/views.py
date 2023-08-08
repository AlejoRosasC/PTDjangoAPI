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

#Api principal / C.R.U.D.
@csrf_exempt
def peticionApi(request,id=0):
    #Metodo GET / muestra todos los registros
   # Verifica si el método de la solicitud es GET
    if request.method == 'GET':

        # Obtiene todos los registros de la base de datos de la entidad Peticion
        peticion = Peticion.objects.all()
        
        # Crea una lista para almacenar las respuestas
        listResponse = []
        # Crea un diccionario para almacenar temporalmente los datos de cada registro
        dictResponse = {}

        # Itera a través de cada registro en la entidad Peticion
        for i in peticion:
            # Asigna los valores del registro actual al diccionario de respuesta
            dictResponse["PeticionId"] = i.PeticionId
            dictResponse["PeticionDate"] = i.PeticionDate
            dictResponse["PeticionMethod"] = i.PeticionMethod
            dictResponse["PeticionConsult"] = i.PeticionConsult
            dictResponse["PeticionDataReturn"] = i.PeticionDataReturn

            # Agrega una copia del diccionario de respuesta a la lista de respuestas
            listResponse.append(dictResponse.copy())

        # Convierte la lista de respuestas a un formato JSON
        response = json.dumps(listResponse)

        # Devuelve una respuesta HTTP con el contenido JSON
        return HttpResponse(response, content_type='application/json')
    
    #Metodo PUT / Edita un registro existente 
    # Verifica si el método de la solicitud es PUT
    if request.method == 'PUT':
        # Analiza los datos JSON enviados en la solicitud
        peticion_data = JSONParser().parse(request)
        
        # Obtiene un objeto Peticion basado en el PeticionId proporcionado en los datos analizados
        peticion = Peticion.objects.get(PeticionId=peticion_data['PeticionId'])
        
        # Inicializa un serializador PeticionSerializer con el objeto Peticion y los datos analizados
        peticion_srlzr = PeticionSerializer(request, data=peticion_data)
        
        # Verifica si los datos del serializador son válidos
        if peticion_srlzr.is_valid():
            # Actualiza los campos del objeto Peticion con los datos analizados
            peticion.PeticionDate = peticion_data['PeticionDate'],
            peticion.PeticionMethod = peticion_data['PeticionMethod'],
            peticion.PeticionConsult = peticion_data['PeticionConsult'],
            peticion.PeticionDataReturn = peticion_data['PeticionDataReturn']
            
            # Guarda los cambios en la base de datos
            peticion.save()

            # Devuelve una respuesta JSON indicando que el registro ha sido modificado
            return JsonResponse("Registro Modificado", safe=False)

    
    #Metodo DELETE / elimina un registro existente
    # Verifica si el método de la solicitud es DELETE
    elif request.method == 'DELETE':
        # Obtiene un objeto Peticion basado en el valor del parámetro "id"
        peticion = Peticion.objects.get(PeticionId=id)
        
        # Elimina el objeto Peticion de la base de datos
        peticion.delete()
        
        # Devuelve una respuesta JSON indicando que el registro ha sido eliminado exitosamente
        return JsonResponse("Deleted Successfully", safe=False)

@csrf_exempt
def mostrarUsuarios(request):
    # Verifica si el método de la solicitud es GET
    if request.method == 'GET':
        # Define el método HTTP y la URL de consulta (endpoint)
        method = "GET"
        url = "https://jsonplaceholder.typicode.com/users"
        
        # Obtiene la marca de tiempo actual
        timestamp = datetime.now()

        # Realiza una solicitud GET a la URL del endpoint
        response = requests.get(url)
        
        # Obtiene los datos de respuesta en formato JSON
        response_data = response.json()

        # Crea un objeto Peticion con la información de la solicitud
        info = Peticion(
            PeticionDate=timestamp.date(),
            PeticionMethod=method,
            PeticionConsult=url,
            PeticionDataReturn=response_data
        )
        
        # Guarda el objeto Peticion en la base de datos
        info.save()

        # Devuelve los datos de respuesta como JSON
        return JsonResponse(response_data, safe=False)
    else:
        # Devuelve una respuesta de error si el método no es GET
        return JsonResponse({"error": "Método no permitido"}, status=405)

    
@csrf_exempt
def mostrarPublicaciones(request):
    # Verifica si el método de la solicitud es GET
    if request.method == 'GET':
        # Define el método HTTP y la URL de consulta (endpoint)
        method = "GET"
        endpoint = "https://jsonplaceholder.typicode.com/posts"
        
        # Obtiene la marca de tiempo actual
        timestamp = datetime.now()

        # Realiza una solicitud GET a la URL del endpoint
        response = requests.get(endpoint)
        
        # Obtiene los datos de respuesta en formato JSON
        response_data = response.json()

        # Crea un objeto Peticion con la información de la solicitud
        info = Peticion(
            PeticionDate=timestamp.date(),
            PeticionMethod=method,
            PeticionConsult=endpoint,
            PeticionDataReturn=response_data
        )
        
        # Guarda el objeto Peticion en la base de datos
        info.save()

        # Devuelve los datos de respuesta como JSON
        return JsonResponse(response_data, safe=False)
    else:
        # Devuelve una respuesta de error si el método no es GET
        return JsonResponse({"error": "Método no permitido"}, status=405)



@csrf_exempt
def fotosPorUsuario(request, id=0):
    # Verifica si el método de la solicitud es GET
    if request.method == 'GET':
        # Define el método HTTP y las URLs de consulta (endpoints)
        method = "GET"
        urlAlbums = f"https://jsonplaceholder.typicode.com/albums?userId={id}"
        urlPhotos = "https://jsonplaceholder.typicode.com/photos?albumId="
        
        # Obtiene la marca de tiempo actual
        timestamp = datetime.now()

        # Realiza una solicitud GET para obtener los albums del usuario
        responseAlbums = requests.get(urlAlbums)
        dataResponseAlbums = responseAlbums.json()

        listaAlbums = []
        listPhotos = []

        # Filtra los albums para obtener solo los del usuario
        for obj in dataResponseAlbums:
            if obj["userId"] == int(id):
                listaAlbums.append(obj["id"])

        # Realiza solicitudes GET para obtener las fotos de cada album
        for id_ in listaAlbums:
            url = urlPhotos + str(id_)
            responsePhotos = requests.get(url)
            dataResponsePhotos = responsePhotos.json()
            listPhotos.extend(dataResponsePhotos)

        # Combina los datos de las fotos en una sola lista
        data = listPhotos

        # Crea un objeto Peticion con la información de la solicitud
        info = Peticion(
            PeticionDate=timestamp.date(),
            PeticionMethod=method,
            PeticionConsult=urlPhotos,
            PeticionDataReturn=data
        )
        
        # Guarda el objeto Peticion en la base de datos
        info.save()

        # Devuelve los datos de fotos como JSON
        return JsonResponse(data, safe=False)
    else:
        # Devuelve una respuesta de error si el método no es GET
        return JsonResponse({"error": "Método no permitido"}, status=405)

