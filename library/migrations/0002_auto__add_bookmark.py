# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Bookmark'
        db.create_table('library_bookmark', (
            ('last_read', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('component', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_modified_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2010, 8, 23, 18, 10, 57, 73243), auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bookmarks', to=orm['auth.User'])),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('percentage', self.gf('django.db.models.fields.DecimalField')(max_digits=25, decimal_places=24)),
            ('archive', self.gf('django.db.models.fields.related.ForeignKey')(related_name='archive', to=orm['library.EpubArchive'])),
        ))
        db.send_create_signal('library', ['Bookmark'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Bookmark'
        db.delete_table('library_bookmark')
    
    
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'library.bookauthor': {
            'Meta': {'object_name': 'BookAuthor'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 8, 23, 18, 10, 57, 73243)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2000'})
        },
        'library.bookmark': {
            'Meta': {'object_name': 'Bookmark'},
            'archive': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'archive'", 'to': "orm['library.EpubArchive']"}),
            'component': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 8, 23, 18, 10, 57, 73243)', 'auto_now': 'True', 'blank': 'True'}),
            'last_read': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'percentage': ('django.db.models.fields.DecimalField', [], {'max_digits': '25', 'decimal_places': '24'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bookmarks'", 'to': "orm['auth.User']"})
        },
        'library.epubarchive': {
            'Meta': {'object_name': 'EpubArchive'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['library.BookAuthor']", 'symmetrical': 'False'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'has_stylesheets': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'db_index': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_viewable': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'db_index': 'True'}),
            'last_chapter_read': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['library.HTMLFile']", 'null': 'True'}),
            'last_modified_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 8, 23, 18, 10, 57, 73243)', 'auto_now': 'True', 'blank': 'True'}),
            'last_nonce': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 8, 23, 18, 10, 57, 77333)'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'opf': ('django.db.models.fields.TextField', [], {}),
            'orderable_author': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'publishers': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['library.EpubPublisher']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'rights': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300'}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['library.Subject']", 'null': 'True', 'symmetrical': 'False', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Untitled'", 'max_length': '5000'}),
            'toc': ('django.db.models.fields.TextField', [], {})
        },
        'library.epubblob': {
            'Meta': {'object_name': 'EpubBlob'},
            'archive': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['library.EpubArchive']"}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idref': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'last_modified_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 8, 23, 18, 10, 57, 73243)', 'auto_now': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'library.epubpublisher': {
            'Meta': {'object_name': 'EpubPublisher'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 8, 23, 18, 10, 57, 73243)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'db_index': 'True'})
        },
        'library.htmlfile': {
            'Meta': {'object_name': 'HTMLFile'},
            'archive': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['library.EpubArchive']"}),
            'content_type': ('django.db.models.fields.CharField', [], {'default': "'application/xhtml'", 'max_length': '100'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idref': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'last_modified_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 8, 23, 18, 10, 57, 73243)', 'auto_now': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'path': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'processed_content': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'stylesheets': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['library.StylesheetFile']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            'words': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        'library.htmlfilemeta': {
            'Meta': {'object_name': 'HTMLFileMeta'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'head_extra': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'htmlfile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['library.HTMLFile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 8, 23, 18, 10, 57, 73243)', 'auto_now': 'True', 'blank': 'True'})
        },
        'library.imageblob': {
            'Meta': {'object_name': 'ImageBlob'},
            'archive': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['library.EpubArchive']"}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idref': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['library.ImageFile']"}),
            'last_modified_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 8, 23, 18, 10, 57, 73243)', 'auto_now': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'library.imagefile': {
            'Meta': {'object_name': 'ImageFile'},
            'archive': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['library.EpubArchive']"}),
            'content_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idref': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'last_modified_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 8, 23, 18, 10, 57, 73243)', 'auto_now': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'library.stylesheetfile': {
            'Meta': {'object_name': 'StylesheetFile'},
            'archive': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['library.EpubArchive']"}),
            'content_type': ('django.db.models.fields.CharField', [], {'default': "'text/css'", 'max_length': '100'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idref': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'last_modified_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 8, 23, 18, 10, 57, 73243)', 'auto_now': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'library.subject': {
            'Meta': {'object_name': 'Subject'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_lcsh': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_modified_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 8, 23, 18, 10, 57, 73243)', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'library.userarchive': {
            'Meta': {'object_name': 'UserArchive'},
            'archive': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_archive'", 'to': "orm['library.EpubArchive']"}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_chapter_read': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['library.HTMLFile']", 'null': 'True'}),
            'last_modified_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 8, 23, 18, 10, 57, 73243)', 'auto_now': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_archive'", 'to': "orm['auth.User']"})
        },
        'library.userpref': {
            'Meta': {'object_name': 'UserPref'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'font_family': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'font_size': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '10'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'last_modified_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 8, 23, 18, 10, 57, 73243)', 'auto_now': 'True', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'open_to_last_chapter': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'simple_reading_mode': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }
    
    complete_apps = ['library']
