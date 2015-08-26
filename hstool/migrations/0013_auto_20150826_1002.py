# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hstool', '0012_auto_20150826_0824'),
    ]

    operations = [
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
        migrations.RemoveField(
            model_name='steepcategory',
            name='short_title',
        ),
        migrations.AlterField(
            model_name='driverofchange',
            name='time_horizon',
            field=models.ForeignKey(related_name=b'driver_time', to='hstool.TimeHorizon'),
        ),
    ]
