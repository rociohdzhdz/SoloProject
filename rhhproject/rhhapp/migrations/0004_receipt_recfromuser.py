# Generated by Django 2.2 on 2020-09-13 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rhhapp', '0003_auto_20200913_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='recfromuser',
            field=models.CharField(default='', max_length=255),
        ),
    ]
