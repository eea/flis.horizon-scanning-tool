# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import hstool.utils


class Migration(migrations.Migration):

    dependencies = [
        ('hstool', '0009_auto_20150805_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='file',
            field=models.FileField(null=True, upload_to=hstool.utils.path_and_rename_sources, blank=True),
        ),
        migrations.AlterField(
            model_name='source',
            name='published_year',
            field=models.CharField(max_length=4),
        ),
        migrations.AlterField(
            model_name='source',
            name='summary',
            field=models.TextField(max_length=2048, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='source',
            name='title_original',
            field=models.CharField(max_length=512, null=True, blank=True),
        ),
    ]
