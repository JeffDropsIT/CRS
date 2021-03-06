# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-25 04:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('face', '0008_auto_20170825_0622'),
    ]

    operations = [
        migrations.AddField(
            model_name='cow',
            name='coat_color',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AddField(
            model_name='cow',
            name='horn_status',
            field=models.CharField(choices=[('Horned In Both Sexes', 'Horned In Both Sexes'), ('Male Only Horned ', 'Male Only Horned ')], default='Horned In Both Sexes', max_length=15),
        ),
        migrations.AddField(
            model_name='cow',
            name='used_for',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='cow',
            name='breed',
            field=models.CharField(choices=[('Jersey', 'Jersey'), ('Aubrac', 'Aubrac')], default='Jersey', max_length=15),
        ),
    ]
