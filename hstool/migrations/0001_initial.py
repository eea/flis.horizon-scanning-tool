# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import hstool.utils
import hstool.models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20150615_1322'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('draft', models.BooleanField(default=True)),
                ('author_id', models.CharField(max_length=64)),
                ('title', models.CharField(max_length=512)),
                ('description', models.TextField(null=True, blank=True)),
                ('added', models.DateTimeField(default=datetime.datetime.now, auto_now_add=True)),
                ('url', models.CharField(max_length=256, null=True, blank=True)),
                ('country', models.ForeignKey(blank=True, to='common.Country', null=True)),
                ('geographical_scope', models.ForeignKey(blank=True, to='common.GeographicalScope', null=True)),
            ],
            options={
                'permissions': (('create', 'Create an assessment'), ('config', 'Can change configuration')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DriverOfChangeType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=64)),
                ('author_id', models.CharField(max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GenericElement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('draft', models.BooleanField(default=True)),
                ('author_id', models.CharField(max_length=64)),
                ('short_name', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=512)),
                ('url', models.CharField(max_length=256, null=True, blank=True)),
                ('added', models.DateTimeField(default=datetime.datetime.now, auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Figure',
            fields=[
                ('genericelement_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='hstool.GenericElement')),
                ('file', hstool.models.ContentTypeRestrictedFileField(upload_to=hstool.utils.path_and_rename_figures)),
            ],
            options={
                'abstract': False,
            },
            bases=('hstool.genericelement', models.Model),
        ),
        migrations.CreateModel(
            name='DriverOfChange',
            fields=[
                ('genericelement_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='hstool.GenericElement')),
                ('trend_type', models.IntegerField(default=1, choices=[(1, b'Trend'), (2, b'Megatrend')])),
                ('uncertainty_type', models.IntegerField(default=1, choices=[(1, b'Rationale'), (2, b'Data'), (3, b'Methodology (related to the model)')])),
                ('summary', models.TextField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('hstool.genericelement', models.Model),
        ),
        migrations.CreateModel(
            name='Impact',
            fields=[
                ('genericelement_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='hstool.GenericElement')),
                ('description', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=('hstool.genericelement', models.Model),
        ),
        migrations.CreateModel(
            name='ImpactType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=64)),
                ('author_id', models.CharField(max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Implication',
            fields=[
                ('genericelement_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='hstool.GenericElement')),
                ('policy_area', models.CharField(default=0, max_length=64, null=True, blank=True, choices=[(b'mock_policy', b'Mock policy')])),
                ('description', models.TextField(max_length=2048)),
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
            ],
            options={
                'abstract': False,
            },
            bases=('hstool.genericelement', models.Model),
        ),
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
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('draft', models.BooleanField(default=True)),
                ('relationship_type', models.IntegerField(blank=True, null=True, choices=[(1, b'Cause-effect relationship'), (2, b'Neutral relationship')])),
                ('description', models.TextField(max_length=2048, null=True, blank=True)),
                ('assessment', models.ForeignKey(related_name=b'relations', to='hstool.Assessment')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('genericelement_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='hstool.GenericElement')),
                ('title_original', models.CharField(max_length=512, null=True, blank=True)),
                ('published_year', models.CharField(max_length=4)),
                ('author', models.CharField(max_length=512)),
                ('file', models.FileField(null=True, upload_to=hstool.utils.path_and_rename_sources, blank=True)),
                ('summary', models.TextField(max_length=2048, null=True, blank=True)),
            ],
            options={
            },
            bases=('hstool.genericelement',),
        ),
        migrations.CreateModel(
            name='SteepCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=64)),
                ('author_id', models.CharField(max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TimeHorizon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=64)),
                ('author_id', models.CharField(max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='relation',
            name='destination',
            field=models.ForeignKey(related_name=b'dest_relations', blank=True, to='hstool.GenericElement'),
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
            model_name='relation',
            name='source',
            field=models.ForeignKey(related_name=b'source_relations', to='hstool.DriverOfChange'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='indicator',
            name='sources',
            field=models.ManyToManyField(to='hstool.Source', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='indicator',
            name='theme',
            field=models.ForeignKey(to='common.EnvironmentalTheme'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='implication',
            name='sources',
            field=models.ManyToManyField(to='hstool.Source', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='impact',
            name='impact_type',
            field=models.ForeignKey(related_name=b'impact_type', blank=True, to='hstool.ImpactType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='impact',
            name='sources',
            field=models.ManyToManyField(to='hstool.Source', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='impact',
            name='steep_category',
            field=models.ForeignKey(related_name=b'impact_category', blank=True, to='hstool.SteepCategory', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='genericelement',
            name='country',
            field=models.ForeignKey(blank=True, to='common.Country', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='genericelement',
            name='geographical_scope',
            field=models.ForeignKey(blank=True, to='common.GeographicalScope', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='figure',
            name='sources',
            field=models.ManyToManyField(to='hstool.Source', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='figure',
            name='theme',
            field=models.ForeignKey(to='common.EnvironmentalTheme'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='driverofchange',
            name='figures',
            field=models.ManyToManyField(to='hstool.Figure', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='driverofchange',
            name='impacts',
            field=models.ManyToManyField(to='hstool.Impact', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='driverofchange',
            name='implications',
            field=models.ManyToManyField(to='hstool.Implication', null=True, blank=True),
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
            model_name='driverofchange',
            name='steep_category',
            field=models.ForeignKey(related_name=b'driver_category', to='hstool.SteepCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='driverofchange',
            name='time_horizon',
            field=models.ForeignKey(related_name=b'driver_time', to='hstool.TimeHorizon'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='driverofchange',
            name='type',
            field=models.ForeignKey(related_name=b'doc_type', to='hstool.DriverOfChangeType'),
            preserve_default=True,
        ),
    ]
