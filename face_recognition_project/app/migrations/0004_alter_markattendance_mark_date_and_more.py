# Generated by Django 4.2.2 on 2023-06-21 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_markattendance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='markattendance',
            name='mark_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='markattendance',
            name='mark_time',
            field=models.TimeField(),
        ),
    ]