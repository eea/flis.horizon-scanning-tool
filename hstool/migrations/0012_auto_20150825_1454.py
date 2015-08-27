# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hstool', '0011_auto_20150825_1247'),
    ]

    operations = [
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
        migrations.AlterField(
            model_name='driverofchange',
            name='type',
            field=models.ForeignKey(related_name=b'doc_type', to='hstool.DriverOfChangeType'),
        ),
    ]
