# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hstool', '0004_auto_20150707_0913'),
    ]

    operations = [
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
        migrations.AlterField(
            model_name='impact',
            name='steep_category',
            field=models.CharField(default=0, max_length=64, null=True, blank=True, choices=[(b'Ec', b'Economic'), (b'Env', b'Environmental'), (b'P', b'Political'), (b'S', b'Social'), (b'T', b'Technological')]),
        ),
    ]
