# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hstool', '0004_auto_20150703_1513'),
    ]

    operations = [
        migrations.RenameField(
            model_name='driverofchange',
            old_name='figures',
            new_name='figureindicators',
        ),
        migrations.RenameField(
            model_name='impact',
            old_name='figures',
            new_name='figureindicators',
        ),
        migrations.RenameField(
            model_name='implication',
            old_name='figures',
            new_name='figureindicators',
        ),
    ]
