# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import hstool.models
import hstool.utils


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20150615_1322'),
        ('hstool', '0006_auto_20150710_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='Figure',
            fields=[
                ('genericelement_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='hstool.GenericElement')),
                ('file', hstool.models.ContentTypeRestrictedFileField(upload_to=hstool.utils.path_and_rename_figures)),
                ('sources', models.ManyToManyField(to='hstool.Source', null=True, blank=True)),
                ('theme', models.ForeignKey(to='common.EnvironmentalTheme')),
            ],
            options={
                'abstract': False,
            },
            bases=('hstool.genericelement', models.Model),
        ),
        migrations.CreateModel(
            name='Indicator',
            fields=[
                ('genericelement_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='hstool.GenericElement')),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField()),
                ('assessment', models.TextField(null=True, blank=True)),
                ('assessment_author', models.CharField(max_length=64, null=True, blank=True)),
                ('file', hstool.models.ContentTypeRestrictedFileField(null=True, upload_to=hstool.utils.path_and_rename_indicators, blank=True)),
                ('sources', models.ManyToManyField(to='hstool.Source', null=True, blank=True)),
                ('theme', models.ForeignKey(to='common.EnvironmentalTheme')),
            ],
            options={
                'abstract': False,
            },
            bases=('hstool.genericelement', models.Model),
        ),
        migrations.RemoveField(
            model_name='figureindicator',
            name='genericelement_ptr',
        ),
        migrations.RemoveField(
            model_name='figureindicator',
            name='theme',
        ),
        migrations.RemoveField(
            model_name='driverofchange',
            name='figureindicators',
        ),
        migrations.RemoveField(
            model_name='genericelement',
            name='sources',
        ),
        migrations.RemoveField(
            model_name='implication',
            name='title',
        ),
        migrations.RemoveField(
            model_name='relation',
            name='figureindicators',
        ),
        migrations.DeleteModel(
            name='FigureIndicator',
        ),
        migrations.RemoveField(
            model_name='source',
            name='added',
        ),
        migrations.RemoveField(
            model_name='source',
            name='author_id',
        ),
        migrations.RemoveField(
            model_name='source',
            name='draft',
        ),
        migrations.RemoveField(
            model_name='source',
            name='id',
        ),
        migrations.RemoveField(
            model_name='source',
            name='title',
        ),
        migrations.RemoveField(
            model_name='source',
            name='url',
        ),
        migrations.AddField(
            model_name='driverofchange',
            name='figures',
            field=models.ManyToManyField(to='hstool.Figure', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='driverofchange',
            name='indicators',
            field=models.ManyToManyField(to='hstool.Indicator', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='driverofchange',
            name='sources',
            field=models.ManyToManyField(to='hstool.Source', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='impact',
            name='sources',
            field=models.ManyToManyField(to='hstool.Source', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='implication',
            name='sources',
            field=models.ManyToManyField(to='hstool.Source', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='relation',
            name='figures',
            field=models.ManyToManyField(to='hstool.Figure', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='relation',
            name='indicators',
            field=models.ManyToManyField(to='hstool.Indicator', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='source',
            name='genericelement_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default='', serialize=False, to='hstool.GenericElement'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='genericelement',
            name='name',
            field=models.CharField(max_length=512),
        ),
        migrations.AlterField(
            model_name='impact',
            name='impact_type',
            field=models.CharField(default=0, max_length=64, null=True, blank=True, choices=[(b'risk', b'Risk'), (b'opportunity', b'Opportunity'), (b'other', b'Other')]),
        ),
    ]
