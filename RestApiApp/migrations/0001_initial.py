# Generated by Django 4.2.4 on 2023-08-07 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Peticion',
            fields=[
                ('PeticionId', models.AutoField(primary_key=True, serialize=False)),
                ('PeticionDate', models.DateField()),
                ('PeticionMethod', models.CharField(max_length=100)),
                ('PeticionConsult', models.CharField(max_length=1000)),
                ('PeticionDataReturn', models.CharField(max_length=10000)),
            ],
        ),
    ]
