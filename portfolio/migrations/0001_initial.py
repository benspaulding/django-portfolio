# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Client'
        db.create_table('portfolio_client', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('portfolio', ['Client'])

        # Adding model 'Testimonial'
        db.create_table('portfolio_testimonial', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(related_name='testimonials', to=orm['portfolio.Client'])),
            ('witness', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('witness_desc', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('testimonial', self.gf('django.db.models.fields.TextField')()),
            ('status', self.gf('portfolio.models.StatusField')(default=1, db_index=True)),
        ))
        db.send_create_signal('portfolio', ['Testimonial'])

        # Adding model 'Medium'
        db.create_table('portfolio_medium', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('portfolio', ['Medium'])

        # Adding model 'Discipline'
        db.create_table('portfolio_discipline', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('portfolio', ['Discipline'])

        # Adding model 'Project'
        db.create_table('portfolio_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('project_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('completion_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('is_ongoing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(related_name='projects', to=orm['portfolio.Client'])),
            ('overview_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('detail_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('status', self.gf('portfolio.models.StatusField')(default=1, db_index=True)),
        ))
        db.send_create_signal('portfolio', ['Project'])

        # Adding M2M table for field media on 'Project'
        db.create_table('portfolio_project_media', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['portfolio.project'], null=False)),
            ('medium', models.ForeignKey(orm['portfolio.medium'], null=False))
        ))
        db.create_unique('portfolio_project_media', ['project_id', 'medium_id'])

        # Adding M2M table for field disciplines on 'Project'
        db.create_table('portfolio_project_disciplines', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['portfolio.project'], null=False)),
            ('discipline', models.ForeignKey(orm['portfolio.discipline'], null=False))
        ))
        db.create_unique('portfolio_project_disciplines', ['project_id', 'discipline_id'])


    def backwards(self, orm):
        # Deleting model 'Client'
        db.delete_table('portfolio_client')

        # Deleting model 'Testimonial'
        db.delete_table('portfolio_testimonial')

        # Deleting model 'Medium'
        db.delete_table('portfolio_medium')

        # Deleting model 'Discipline'
        db.delete_table('portfolio_discipline')

        # Deleting model 'Project'
        db.delete_table('portfolio_project')

        # Removing M2M table for field media on 'Project'
        db.delete_table('portfolio_project_media')

        # Removing M2M table for field disciplines on 'Project'
        db.delete_table('portfolio_project_disciplines')


    models = {
        'portfolio.client': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Client'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'portfolio.discipline': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Discipline'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'portfolio.medium': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Medium'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'portfolio.project': {
            'Meta': {'ordering': "('-completion_date', 'name')", 'object_name': 'Project'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'to': "orm['portfolio.Client']"}),
            'completion_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'detail_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'disciplines': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'projects'", 'symmetrical': 'False', 'to': "orm['portfolio.Discipline']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_ongoing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'media': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'projects'", 'symmetrical': 'False', 'to': "orm['portfolio.Medium']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'overview_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'project_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'status': ('portfolio.models.StatusField', [], {'default': '1', 'db_index': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'portfolio.testimonial': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Testimonial'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'testimonials'", 'to': "orm['portfolio.Client']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('portfolio.models.StatusField', [], {'default': '1', 'db_index': 'True'}),
            'testimonial': ('django.db.models.fields.TextField', [], {}),
            'witness': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'witness_desc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['portfolio']
