# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-25 04:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('face', '0006_auto_20170825_0617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cattlelog',
            name='birth_date',
            field=models.DateTimeField(),
        ),
    ]
