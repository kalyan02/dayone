from django.db import models
from django.contrib import admin, auth
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib import admin
import time, json

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^do\.models\.JSONField"])

class JSONField(models.TextField):
	def to_python(self,value):
		return json.loads(value)

	def get_prep_value(self,value):
		return json.dumps(value)

class Profile(models.Model):
	user = models.OneToOneField(auth.models.User)

	# relative to l
	journal_path = models.CharField(max_length=200,null=True,default='',blank=True)
	journal_share_url = models.CharField(max_length=200,null=True,default='',blank=True)

	photos_path = models.CharField(max_length=200,null=True,default='',blank=True)
	photos_share_url = models.CharField(max_length=200,null=True,default='',blank=True)

	entries_path = models.CharField(max_length=200,null=True,default='',blank=True)
	entries_share_url = models.CharField(max_length=200,null=True,default='',blank=True)

	pub_tag = models.CharField(max_length=200,default='public')

	entries_meta = models.TextField(default=None,null=True,blank=True)
	entries_last_sync = models.IntegerField(db_index=True,default=0)

class Post(models.Model):
	user = models.ForeignKey(auth.models.User)
	entry_path = models.CharField(max_length=200,null=True,default='',blank=True)
	entry_share_url = models.CharField(max_length=200,null=True,default='',blank=True)
	content = models.TextField(default=None,null=True)
	sync_complete = models.BooleanField(default=False)

	uuid = models.CharField(max_length=64,null=True,default='',blank=True)
	pub_date = models.DateField(null=True)
	all_tags = models.TextField(default=None,null=True)


class UserStatusFactory:
	def __init__(self,_base_class,_user_object):
		self._user_object = _user_object
		self._base_class = _base_class
	def get(self,*kargs,**kwargs):
		return self._base_class.get(self._user_object,*kargs,**kwargs)
	def set(self,*kargs,**kwargs):
		return self._base_class.set(self._user_object,*kargs,**kwargs)

# TODO: Tie this model to a redis instance for faster access
class Status(models.Model):
	user = models.ForeignKey(auth.models.User)
	key = models.CharField(max_length=64,null=True)
	value = models.CharField(max_length=64,blank=True,null=True)

	@classmethod
	def factory(_status_class,_user):
		return UserStatusFactory(_status_class,_user)

	@classmethod
	def get(_class,_user,_key):
		try:
			return _class.objects.get(user=_user,key=_key)
		except:
			return _class.objects.create(user=_user,key=_key)

	@classmethod
	def set(_class,_user,_key,_value):
		obj = _class.get(_user,_key)
		# TODO:
		# if _value == False or _value == None: obj.delete() ????
		obj.value = _value
		obj.save()


admin.site.register(Profile,admin.ModelAdmin)
admin.site.register(Post,admin.ModelAdmin)
admin.site.register(Status,admin.ModelAdmin)
