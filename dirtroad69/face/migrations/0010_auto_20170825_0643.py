# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-25 04:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('face', '0009_auto_20170825_0642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cow',
            name='horn_status',
            field=models.CharField(choices=[('Horned In Both Sexes', 'Horned In Both Sexes'), ('Male Only Horned ', 'Male Only Horned ')], default='Horned In Both Sexes', max_length=50),
        ),
    ]
