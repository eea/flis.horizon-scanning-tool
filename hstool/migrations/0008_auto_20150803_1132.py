# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hstool', '0007_auto_20150803_1132'),
    ]

    operations = [
        migrations.AddField(
            model_name='driverofchange',
            name='sources',
            field=models.ManyToManyField(to='hstool.Source', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='figure',
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
            model_name='indicator',
            name='sources',
            field=models.ManyToManyField(to='hstool.Source', null=True, blank=True),
            preserve_default=True,
        ),
    ]
