# Generated by Django 4.2.2 on 2023-06-21 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_markattendance_shift'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='markattendance',
            name='employee_id',
        ),
        migrations.RemoveField(
            model_name='markattendance',
            name='mark_date',
        ),
    ]