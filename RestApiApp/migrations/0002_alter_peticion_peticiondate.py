# Generated by Django 4.2.4 on 2023-08-07 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestApiApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peticion',
            name='PeticionDate',
            field=models.CharField(max_length=100),
        ),
    ]
