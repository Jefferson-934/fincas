# Generated by Django 3.1.7 on 2021-08-28 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='cedula',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='expediente',
            name='finca',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.finca'),
        ),
        migrations.AlterField(
            model_name='finca',
            name='nombre_finca',
            field=models.CharField(max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='planta',
            name='nombre_planta',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
