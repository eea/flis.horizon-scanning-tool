# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.core.management import call_command
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        call_command('load_metadata_fixtures')
        for generic_elem in orm.GenericElement.objects.all():
            geo_scope = generic_elem.geographical_scope
            geo_scope_title = geo_scope.title if geo_scope else None
            model = orm['common.GeographicalScope']
            try:
                fake_geo_scope = model.objects.get(title=geo_scope_title)
                generic_elem.fake_geographical_scope = fake_geo_scope
            except model.DoesNotExist:
                pass

            country = generic_elem.country
            country_name = country.name if country else None
            model = orm['common.Country']
            try:
                fake_country = model.objects.get(name=country_name)
                generic_elem.fake_country = fake_country
            except model.DoesNotExist:
                pass
            generic_elem.save()

        for indicator in orm.Indicator.objects.all():
            env_theme = indicator.theme
            theme_title = env_theme.title if env_theme else None
            model = orm['common.EnvironmentalTheme']
            try:
                fake_theme = model.objects.get(title=theme_title)
                indicator.fake_theme = fake_theme
            except model.DoesNotExist:
                pass
            indicator.save()

    def backwards(self, orm):
        raise RuntimeError("This migration can't be undone")

    models = {
        u'common.country': {
            'Meta': {'object_name': 'Country'},
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'iso': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'common.environmentaltheme': {
            'Meta': {'ordering': "('-pk',)", 'object_name': 'EnvironmentalTheme'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'common.geographicalscope': {
            'Meta': {'ordering': "('-pk',)", 'object_name': 'GeographicalScope'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'require_country': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'hstool.assessment': {
            'Meta': {'object_name': 'Assessment'},
            'added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'author_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'hstool.country': {
            'Meta': {'object_name': 'Country'},
            'iso': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'hstool.driverofchange': {
            'Meta': {'object_name': 'DriverOfChange', '_ormbases': [u'hstool.GenericElement']},
            u'genericelement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['hstool.GenericElement']", 'unique': 'True', 'primary_key': 'True'}),
            'steep_category': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'time_horizon': ('django.db.models.fields.IntegerField', [], {}),
            'trend_type': ('django.db.models.fields.IntegerField', [], {}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        u'hstool.environmentaltheme': {
            'Meta': {'ordering': "('-pk',)", 'object_name': 'EnvironmentalTheme'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'hstool.figure': {
            'Meta': {'object_name': 'Figure'},
            'added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'author_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'file': ('hstool.models.ContentTypeRestrictedFileField', [], {'content_types': ['application/pdf', 'image/jpg', 'image/jpeg']}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512'})
        },
        u'hstool.genericelement': {
            'Meta': {'object_name': 'GenericElement'},
            'added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'author_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hstool.Country']", 'null': 'True', 'blank': 'True'}),
            'fake_country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Country']", 'null': 'True', 'blank': 'True'}),
            'fake_geographical_scope': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.GeographicalScope']", 'null': 'True', 'blank': 'True'}),
            'figures': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['hstool.Figure']", 'null': 'True', 'blank': 'True'}),
            'geographical_scope': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hstool.GeographicalScope']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'sources': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['hstool.Source']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
        },
        u'hstool.geographicalscope': {
            'Meta': {'ordering': "('-pk',)", 'object_name': 'GeographicalScope'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'require_country': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'hstool.indicator': {
            'Meta': {'object_name': 'Indicator', '_ormbases': [u'hstool.GenericElement']},
            'fake_theme': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.EnvironmentalTheme']", 'null': 'True', 'blank': 'True'}),
            u'genericelement_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['hstool.GenericElement']", 'unique': 'True', 'primary_key': 'True'}),
            'theme': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hstool.EnvironmentalTheme']"}),
            'timeline': ('django.db.models.fields.IntegerField', [], {}),
            'year_base': ('django.db.models.fields.IntegerField', [], {}),
            'year_end': ('django.db.models.fields.IntegerField', [], {})
        },
        u'hstool.relation': {
            'Meta': {'object_name': 'Relation'},
            'assessment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relations'", 'to': u"orm['hstool.Assessment']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2048'}),
            'destination': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dest_relations'", 'to': u"orm['hstool.GenericElement']"}),
            'figures': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['hstool.Figure']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relationship_type': ('django.db.models.fields.IntegerField', [], {}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'source_relations'", 'to': u"orm['hstool.GenericElement']"})
        },
        u'hstool.source': {
            'Meta': {'object_name': 'Source'},
            'added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'author_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published_year': ('django.db.models.fields.IntegerField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {'max_length': '2048'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'title_original': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['hstool']
    symmetrical = True
