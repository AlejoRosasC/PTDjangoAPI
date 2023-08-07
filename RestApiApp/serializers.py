from rest_framework import serializers
from RestApiApp.models import Peticion

class PeticionSerializer(serializers.Serializer):
    class Meta:
            model=Peticion
            fields=('PeticionId','PeticionDate', 'PeticionMethod', 'PeticionConsult', 'PeticionDataReturn')