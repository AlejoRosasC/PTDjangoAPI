from django.db import models

# Create your models here.
class Peticion(models.Model):
    PeticionId = models.AutoField(primary_key=True)
    PeticionDate = models.CharField(max_length=100, null=False)
    PeticionMethod = models.CharField(max_length=100, null=False)
    PeticionConsult = models.CharField(max_length=1000, null=False)
    PeticionDataReturn = models.CharField(max_length=10000, null=False)