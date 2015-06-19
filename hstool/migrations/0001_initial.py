# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import hstool.models
import hstool.utils


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
            name='Figure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('draft', models.BooleanField(default=True)),
                ('author_id', models.CharField(max_length=64)),
                ('title', models.CharField(default=b'', max_length=512)),
                ('file', hstool.models.ContentTypeRestrictedFileField(upload_to=hstool.utils.path_and_rename_figures)),
                ('added', models.DateTimeField(default=datetime.datetime.now, auto_now_add=True)),
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
                ('name', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=256, null=True, blank=True)),
                ('added', models.DateTimeField(default=datetime.datetime.now, auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DriverOfChange',
            fields=[
                ('genericelement_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='hstool.GenericElement')),
                ('type', models.IntegerField(choices=[(1, b'Trends'), (2, b'Uncertainties'), (3, b'Wild Cards'), (4, b'Weak signals')])),
                ('trend_type', models.IntegerField(default=1, choices=[(1, b'Trend'), (2, b'Megatrend')])),
                ('uncertainty_type', models.IntegerField(default=1, choices=[(1, b'Rationale'), (2, b'Data'), (3, b'Methodology (related to the model)')])),
                ('steep_category', models.CharField(max_length=5, choices=[(b'Ec', b'Economic'), (b'Env', b'Environmental'), (b'P', b'Political'), (b'S', b'Social'), (b'T', b'Technological')])),
                ('time_horizon', models.IntegerField(choices=[(1, b'1 year'), (5, b'5 years'), (10, b'10 years'), (50, b'50 years'), (100, b'100 years'), (200, b'more than 100 years')])),
                ('summary', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=('hstool.genericelement',),
        ),
        migrations.CreateModel(
            name='Implication',
            fields=[
                ('genericelement_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='hstool.GenericElement')),
                ('title', models.CharField(max_length=512)),
                ('policy_area', models.CharField(default=0, max_length=64, null=True, blank=True, choices=[(b'mock_policy', b'Mock policy')])),
                ('description', models.TextField(max_length=2048)),
            ],
            options={
            },
            bases=('hstool.genericelement',),
        ),
        migrations.CreateModel(
            name='Indicator',
            fields=[
                ('genericelement_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='hstool.GenericElement')),
                ('year_base', models.IntegerField()),
                ('year_end', models.IntegerField()),
                ('timeline', models.IntegerField(choices=[(5, b'5-year intermediate'), (0, b'continuous'), (1, b'daily'), (2, b'monthly'), (3, b'point'), (4, b'weekly'), (6, b'yearly')])),
                ('theme', models.ForeignKey(to='common.EnvironmentalTheme')),
            ],
            options={
            },
            bases=('hstool.genericelement',),
        ),
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('draft', models.BooleanField(default=True)),
                ('relationship_type', models.IntegerField(choices=[(1, b'Cause-effect relationship'), (2, b'Neutral relationship')])),
                ('description', models.TextField(max_length=2048)),
                ('assessment', models.ForeignKey(related_name=b'relations', to='hstool.Assessment')),
                ('destination', models.ForeignKey(related_name=b'dest_relations', to='hstool.GenericElement')),
                ('figures', models.ManyToManyField(to='hstool.Figure', null=True, blank=True)),
                ('source', models.ForeignKey(related_name=b'source_relations', to='hstool.GenericElement')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('draft', models.BooleanField(default=True)),
                ('author_id', models.CharField(max_length=64)),
                ('title', models.CharField(max_length=512)),
                ('title_original', models.CharField(max_length=512)),
                ('published_year', models.IntegerField()),
                ('author', models.CharField(max_length=512)),
                ('url', models.CharField(max_length=256)),
                ('file', models.FileField(upload_to=hstool.utils.path_and_rename_sources)),
                ('summary', models.TextField(max_length=2048)),
                ('added', models.DateTimeField(default=datetime.datetime.now, auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='genericelement',
            name='country',
            field=models.ForeignKey(blank=True, to='common.Country', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='genericelement',
            name='figures',
            field=models.ManyToManyField(to='hstool.Figure', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='genericelement',
            name='geographical_scope',
            field=models.ForeignKey(blank=True, to='common.GeographicalScope', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='genericelement',
            name='sources',
            field=models.ManyToManyField(to='hstool.Source', null=True, blank=True),
            preserve_default=True,
        ),
    ]
