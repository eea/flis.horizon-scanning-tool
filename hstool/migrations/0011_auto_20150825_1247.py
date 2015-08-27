# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hstool', '0010_auto_20150812_1413'),
    ]

    operations = [
        migrations.CreateModel(
            name='SteepCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=64)),
                ('short_title', models.CharField(max_length=5)),
                ('author_id', models.CharField(max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='driverofchange',
            name='steep_category',
            field=models.ForeignKey(related_name=b'driver_category', to='hstool.SteepCategory'),
        ),
        migrations.AlterField(
            model_name='impact',
            name='steep_category',
            field=models.ForeignKey(related_name=b'impact_category', blank=True, to='hstool.SteepCategory', null=True),
        ),
    ]
