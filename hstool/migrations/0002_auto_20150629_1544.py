# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hstool', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relation',
            name='destination',
            field=models.ForeignKey(related_name=b'dest_relations', blank=True, to='hstool.GenericElement'),
        ),
        migrations.AlterField(
            model_name='relation',
            name='source',
            field=models.ForeignKey(related_name=b'source_relations', to='hstool.DriverOfChange'),
        ),
    ]
