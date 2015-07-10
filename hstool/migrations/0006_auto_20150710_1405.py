# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hstool', '0005_auto_20150708_0924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='impact',
            name='figureindicators',
        ),
        migrations.RemoveField(
            model_name='implication',
            name='figureindicators',
        ),
    ]
