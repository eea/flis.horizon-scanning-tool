# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import hstool.utils
import hstool.models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20150615_1322'),
        ('hstool', '0003_impact'),
    ]

    operations = [
        migrations.CreateModel(
            name='FigureIndicator',
            fields=[
                ('genericelement_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='hstool.GenericElement')),
                ('is_indicator', models.BooleanField(default=False)),
                ('title', models.CharField(default=b'', max_length=512)),
                ('file', hstool.models.ContentTypeRestrictedFileField(upload_to=hstool.utils.path_and_rename_figures)),
                ('theme', models.ForeignKey(to='common.EnvironmentalTheme')),
            ],
            options={
            },
            bases=('hstool.genericelement',),
        ),
        migrations.RemoveField(
            model_name='indicator',
            name='genericelement_ptr',
        ),
        migrations.RemoveField(
            model_name='indicator',
            name='theme',
        ),
        migrations.DeleteModel(
            name='Indicator',
        ),
        migrations.RemoveField(
            model_name='genericelement',
            name='figures',
        ),
        migrations.RemoveField(
            model_name='relation',
            name='figures',
        ),
        migrations.DeleteModel(
            name='Figure',
        ),
        migrations.AddField(
            model_name='driverofchange',
            name='figures',
            field=models.ManyToManyField(to='hstool.FigureIndicator', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='impact',
            name='figures',
            field=models.ManyToManyField(to='hstool.FigureIndicator', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='implication',
            name='figures',
            field=models.ManyToManyField(to='hstool.FigureIndicator', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='relation',
            name='figureindicators',
            field=models.ManyToManyField(to='hstool.FigureIndicator', null=True, blank=True),
            preserve_default=True,
        ),
    ]
