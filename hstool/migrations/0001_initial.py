# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EnvironmentalTheme'
        db.create_table(u'hstool_environmentaltheme', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'hstool', ['EnvironmentalTheme'])

        # Adding model 'GeographicalScope'
        db.create_table(u'hstool_geographicalscope', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('require_country', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'hstool', ['GeographicalScope'])

        # Adding model 'Country'
        db.create_table(u'hstool_country', (
            ('iso', self.gf('django.db.models.fields.CharField')(max_length=2, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'hstool', ['Country'])

        # Adding model 'Figure'
        db.create_table(u'hstool_figure', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author_id', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=512)),
            ('file', self.gf('hstool.ContentTypeRestrictedFileField')(content_types=['application/pdf', 'image/jpg', 'image/jpeg'], upload_to=<function wrapper at 0x109e32a28>)),
        ))
        db.send_create_signal(u'hstool', ['Figure'])

        # Adding model 'Source'
        db.create_table(u'hstool_source', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author_id', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('title_original', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('published_year', self.gf('django.db.models.fields.IntegerField')()),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('summary', self.gf('django.db.models.fields.TextField')(max_length=2048)),
        ))
        db.send_create_signal(u'hstool', ['Source'])

        # Adding model 'GenericElement'
        db.create_table(u'hstool_genericelement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author_id', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('geographical_scope', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hstool.GeographicalScope'], null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hstool.Country'], null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal(u'hstool', ['GenericElement'])

        # Adding M2M table for field sources on 'GenericElement'
        m2m_table_name = db.shorten_name(u'hstool_genericelement_sources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('genericelement', models.ForeignKey(orm[u'hstool.genericelement'], null=False)),
            ('source', models.ForeignKey(orm[u'hstool.source'], null=False))
        ))
        db.create_unique(m2m_table_name, ['genericelement_id', 'source_id'])

        # Adding M2M table for field figures on 'GenericElement'
        m2m_table_name = db.shorten_name(u'hstool_genericelement_figures')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('genericelement', models.ForeignKey(orm[u'hstool.genericelement'], null=False)),
            ('figure', models.ForeignKey(orm[u'hstool.figure'], null=False))
        ))
        db.create_unique(m2m_table_name, ['genericelement_id', 'figure_id'])

        # Adding model 'DriverOfChange'
        db.create_table(u'hstool_driverofchange', (
            (u'genericelement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hstool.GenericElement'], unique=True, primary_key=True)),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('trend_type', self.gf('django.db.models.fields.IntegerField')()),
            ('steep_category', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('time_horizon', self.gf('django.db.models.fields.IntegerField')()),
            ('summary', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'hstool', ['DriverOfChange'])

        # Adding model 'Indicator'
        db.create_table(u'hstool_indicator', (
            (u'genericelement_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['hstool.GenericElement'], unique=True, primary_key=True)),
            ('theme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hstool.EnvironmentalTheme'])),
            ('year_base', self.gf('django.db.models.fields.IntegerField')()),
            ('year_end', self.gf('django.db.models.fields.IntegerField')()),
            ('timeline', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'hstool', ['Indicator'])

        # Adding model 'Relation'
        db.create_table(u'hstool_relation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('assessment', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relations', to=orm['hstool.Assessment'])),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='source_relations', to=orm['hstool.GenericElement'])),
            ('destination', self.gf('django.db.models.fields.related.ForeignKey')(related_name='dest_relations', to=orm['hstool.GenericElement'])),
            ('relationship_type', self.gf('django.db.models.fields.IntegerField')()),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=2048)),
        ))
        db.send_create_signal(u'hstool', ['Relation'])

        # Adding M2M table for field figures on 'Relation'
        m2m_table_name = db.shorten_name(u'hstool_relation_figures')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('relation', models.ForeignKey(orm[u'hstool.relation'], null=False)),
            ('figure', models.ForeignKey(orm[u'hstool.figure'], null=False))
        ))
        db.create_unique(m2m_table_name, ['relation_id', 'figure_id'])

        # Adding model 'Assessment'
        db.create_table(u'hstool_assessment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author_id', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'hstool', ['Assessment'])


    def backwards(self, orm):
        # Deleting model 'EnvironmentalTheme'
        db.delete_table(u'hstool_environmentaltheme')

        # Deleting model 'GeographicalScope'
        db.delete_table(u'hstool_geographicalscope')

        # Deleting model 'Country'
        db.delete_table(u'hstool_country')

        # Deleting model 'Figure'
        db.delete_table(u'hstool_figure')

        # Deleting model 'Source'
        db.delete_table(u'hstool_source')

        # Deleting model 'GenericElement'
        db.delete_table(u'hstool_genericelement')

        # Removing M2M table for field sources on 'GenericElement'
        db.delete_table(db.shorten_name(u'hstool_genericelement_sources'))

        # Removing M2M table for field figures on 'GenericElement'
        db.delete_table(db.shorten_name(u'hstool_genericelement_figures'))

        # Deleting model 'DriverOfChange'
        db.delete_table(u'hstool_driverofchange')

        # Deleting model 'Indicator'
        db.delete_table(u'hstool_indicator')

        # Deleting model 'Relation'
        db.delete_table(u'hstool_relation')

        # Removing M2M table for field figures on 'Relation'
        db.delete_table(db.shorten_name(u'hstool_relation_figures'))

        # Deleting model 'Assessment'
        db.delete_table(u'hstool_assessment')


    models = {
        u'hstool.assessment': {
            'Meta': {'object_name': 'Assessment'},
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
            'author_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'file': ('hstool.ContentTypeRestrictedFileField', [], {'content_types': ['application/pdf', 'image/jpg', 'image/jpeg'], 'upload_to': <function wrapper at 0x109e32a28>}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512'})
        },
        u'hstool.genericelement': {
            'Meta': {'object_name': 'GenericElement'},
            'author_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hstool.Country']", 'null': 'True', 'blank': 'True'}),
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