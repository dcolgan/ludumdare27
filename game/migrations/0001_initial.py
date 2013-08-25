# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Account'
        db.create_table(u'game_account', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('team', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('has_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('col', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('row', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('last_col', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('last_row', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('last_direction', self.gf('django.db.models.fields.CharField')(default='south', max_length=10)),
            ('direction', self.gf('django.db.models.fields.CharField')(default='south', max_length=10)),
            ('last_chat_message', self.gf('django.db.models.fields.CharField')(default='', max_length=75, blank=True)),
            ('chat_message', self.gf('django.db.models.fields.CharField')(default='', max_length=75, blank=True)),
            ('flags_gotten', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('enemies_tagged', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('actions', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('last_actions', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('stamina', self.gf('django.db.models.fields.IntegerField')(default=20)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'game', ['Account'])

        # Adding M2M table for field groups on 'Account'
        m2m_table_name = db.shorten_name(u'game_account_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('account', models.ForeignKey(orm[u'game.account'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['account_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'Account'
        m2m_table_name = db.shorten_name(u'game_account_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('account', models.ForeignKey(orm[u'game.account'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['account_id', 'permission_id'])

        # Adding model 'Square'
        db.create_table(u'game_square', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('col', self.gf('django.db.models.fields.IntegerField')()),
            ('row', self.gf('django.db.models.fields.IntegerField')()),
            ('terrain_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('tile', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'game', ['Square'])

        # Adding model 'Log'
        db.create_table(u'game_log', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('col', self.gf('django.db.models.fields.IntegerField')()),
            ('row', self.gf('django.db.models.fields.IntegerField')()),
            ('team', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('has_flag', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'game', ['Log'])


    def backwards(self, orm):
        # Deleting model 'Account'
        db.delete_table(u'game_account')

        # Removing M2M table for field groups on 'Account'
        db.delete_table(db.shorten_name(u'game_account_groups'))

        # Removing M2M table for field user_permissions on 'Account'
        db.delete_table(db.shorten_name(u'game_account_user_permissions'))

        # Deleting model 'Square'
        db.delete_table(u'game_square')

        # Deleting model 'Log'
        db.delete_table(u'game_log')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'game.account': {
            'Meta': {'object_name': 'Account'},
            'actions': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'chat_message': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '75', 'blank': 'True'}),
            'col': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'direction': ('django.db.models.fields.CharField', [], {'default': "'south'", 'max_length': '10'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'enemies_tagged': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'flags_gotten': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'has_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_actions': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'last_chat_message': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '75', 'blank': 'True'}),
            'last_col': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'last_direction': ('django.db.models.fields.CharField', [], {'default': "'south'", 'max_length': '10'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_row': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'row': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'stamina': ('django.db.models.fields.IntegerField', [], {'default': '20'}),
            'team': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'game.log': {
            'Meta': {'object_name': 'Log'},
            'col': ('django.db.models.fields.IntegerField', [], {}),
            'has_flag': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'row': ('django.db.models.fields.IntegerField', [], {}),
            'team': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'game.square': {
            'Meta': {'object_name': 'Square'},
            'col': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'row': ('django.db.models.fields.IntegerField', [], {}),
            'terrain_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'tile': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['game']