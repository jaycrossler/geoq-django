# -*- coding: utf-8 -*-

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, as long as
# any reuse or further development of the software attributes the
# National Geospatial-Intelligence Agency (NGA) auhtorship as follows:
# 'This software (GeoQ or Geographic Work Queueing and Tasking System)
# is provided to the public as a courtesy of the National
# Geospatial-Intelligence Agency.
#  
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#  
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    depends_on = (
        ("maps", "0002_auto__add_feature"),
        ("maps", "0003_auto__add_featuretype__del_field_feature_geometry__add_field_feature_t"),
    )

    def forwards(self, orm):
        # Adding field 'Job.map'
        db.add_column(u'core_job', 'map',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maps.Map'], null=True, blank=True),
                      keep_default=False)

        # Adding M2M table for field feature_types on 'Job'
        m2m_table_name = db.shorten_name(u'core_job_feature_types')
        m2m_table_name = db.shorten_name(u'core_job_feature_types')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('job', models.ForeignKey(orm[u'core.job'], null=False)),
            ('featuretype', models.ForeignKey(orm[u'maps.featuretype'], null=False))
        ))
        db.create_unique(m2m_table_name, ['job_id', 'featuretype_id'])


    def backwards(self, orm):
        # Deleting field 'Job.map'
        db.delete_column(u'core_job', 'map_id')

        # Removing M2M table for field feature_types on 'Job'
        db.delete_table(db.shorten_name(u'core_job_feature_types'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.aoi': {
            'Meta': {'object_name': 'AOI'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'analyst': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'aois'", 'to': u"orm['core.Job']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'polygon': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'priority': ('django.db.models.fields.SmallIntegerField', [], {'default': '5', 'max_length': '1'}),
            'reviewers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'aoi_reviewers'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Unassigned'", 'max_length': '15'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'core.job': {
            'Meta': {'ordering': "('-created_at',)", 'object_name': 'Job'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'analysts': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'analysts'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'feature_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['maps.FeatureType']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['maps.Map']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'progress': ('django.db.models.fields.SmallIntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project'", 'to': u"orm['core.Project']"}),
            'reviewers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'reviewers'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'core.project': {
            'Meta': {'ordering': "('-created_at',)", 'object_name': 'Project'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'project_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'maps.featuretype': {
            'Meta': {'object_name': 'FeatureType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'properties': ('jsonfield.fields.JSONField', [], {}),
            'style': ('jsonfield.fields.JSONField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        u'maps.map': {
            'Meta': {'object_name': 'Map'},
            'center_x': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'center_y': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '800', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'projection': ('django.db.models.fields.CharField', [], {'default': "'EPSG:4326'", 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'zoom': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['core']