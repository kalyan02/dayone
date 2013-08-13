import time
from time import sleep

from celery import task, current_task
from celery.result import AsyncResult

from django.http import HttpResponse, HttpResponseRedirect
import lib, settings
import urllib, json

#should spawn more tasks to fetch individual posts
@task
def sync_meta( user_profile, *kargs ):
	time.sleep(1)
	# dapi = lib.DropboxAPI( user=user_profile.user )
	# req = dapi.request('https://api.dropbox.com/1/metadata/dropbox/' + user_profile.entries_path ).to_url()
	# eres = urllib.urlopen(req).read()
	# eres_obj = json.loads( eres )
	# eres_obj = json.loads( user_profile.entries_meta )

	# first fetch share_url -> this gives us the direct links
	# put it in session


	# user_profile.entries_meta = eres
	# user_profile.entries_last_sync = time.time()
	# user_profile.save()

	# trigger post_refresh_in_progress=True

	print "lets see", user_profile.entries_path
	print user_profile.user.first_name
	return str(kargs)
	pass

@task
def sync_data():
	pass

@task
def sync_post():
	pass