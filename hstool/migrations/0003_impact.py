# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hstool', '0002_auto_20150629_1544'),
    ]

    operations = [
        migrations.CreateModel(
            name='Impact',
            fields=[
                ('genericelement_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='hstool.GenericElement')),
                ('impact_type', models.CharField(default=0, max_length=64, null=True, blank=True, choices=[(b'opportunity', b'Opportunity'), (b'other', b'Other')])),
                ('steep_category', models.CharField(default=0, max_length=64, null=True, blank=True, choices=[(b'economic', b'Ec (Economic)'), (b'env', b'Env (Environmental)'), (b'political', b'P (Political)'), (b'social', b'S (Social)'), (b'tech', b'T (Technological)')])),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=('hstool.genericelement',),
        ),
    ]
