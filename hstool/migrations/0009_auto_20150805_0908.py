# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import hstool.utils


class Migration(migrations.Migration):

    dependencies = [
        ('hstool', '0008_auto_20150803_1132'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndicatorFiles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(null=True, upload_to=hstool.utils.path_and_rename_indicators, blank=True)),
                ('indicator', models.ForeignKey(to='hstool.Indicator')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='indicator',
            name='file',
        ),
    ]
