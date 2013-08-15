from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.http import HttpResponse
from django.forms import models, ModelForm, HiddenInput
from do.models import *
from django.db import connection
from django.contrib.auth.decorators import login_required
from django import forms
from django.forms.util import ErrorList
from django.template.loader import render_to_string

import oauth2, json, urlparse, urllib, time, os

from do import settings, lib, tasks

class EditProfileForm(forms.Form):
	pub_tag = forms.CharField()
	anon_tag = forms.CharField()

def _get_request_user_profile(request):
	try:
		user_profile = Profile.objects.get(user_id=request.user.id)
	except:
		user_profile = Profile.objects.create(user_id=request.user.id)

	return user_profile

def _get_user_status(request):
	try:
		user_status = Status.objects.get(user_id=request.user.id)
	except:
		user_status = Status.objects.create(user_id=request.user.id)

@login_required(login_url='/')
def edit_profile(request):
	user_profile = _get_request_user_profile(request)

	if request.POST:
		form = EditProfileForm(data=request.POST)
		if form.is_valid():
			user_profile.pub_tag = form.cleaned_data['pub_tag']
			user_profile.anon_tag = form.cleaned_data['anon_tag']
			user_profile.save()

			tasks.sync_meta.delay( user_profile )
	else:
		form = EditProfileForm(initial={
				'pub_tag':user_profile.pub_tag,
				'anon_tag':user_profile.anon_tag
			})
		form.user = request.user

	return render( request, 'edit_profile.html', {
			'user' : request.user,
			'form' : form,
			'queries' : connection.queries
		})

@login_required(login_url='/')
def api_profile(request):
	profile = request.user.profile
	meta = json.loads(profile.entries_meta)
	items = meta['contents']
	obj = [ os.path.basename(item['path']) for item in items ]


	return HttpResponse(json.dumps(obj))
	pass

@login_required(login_url='/')
def auth_complete(request):
	# check if user has completed setup
	try:
		user = request.user
		profile = user.profile
		if not profile.journal_path or len(profile.journal_path) == 0:
			return redirect('/setup_profile')
	except Exception, e:
		return HttpResponse( e.message )

	return redirect('/edit_profile')

	pass

class SetupProfile_SelectPath_Form(forms.Form):
	path_index = forms.IntegerField()


@login_required(login_url='/')
def setup_profile(request):
	# check if user has completed setup

	user_profile = _get_request_user_profile(request)

	dapi = lib.DropboxAPI( user=request.user )
	res_obj = request.session.get('dayone_search_listing', False)
	if not res_obj:
		print 'new session'
		req = dapi.request('https://api.dropbox.com/1/search/dropbox/', {'query':'.dayone'} ).to_url()
		res = urllib.urlopen(req).read()

		res_obj = json.loads( res )
		res_obj = filter( lambda item : item['is_dir'] == True and item['path'].endswith(".dayone"), res_obj )
		for i, item in enumerate(res_obj):
			item['i'] = str(i)
		request.session['dayone_search_listing'] = res_obj

	metadata = ''
	if request.POST:
		form = SetupProfile_SelectPath_Form(data=request.POST)
		if form.is_valid():
			try:
				form_path_index = int(form.cleaned_data['path_index'])
				if form_path_index <= len(res_obj):
					path_obj = res_obj[ form_path_index ]
					journal_path = path_obj['path'].strip('/')
					entries_path = path_obj['path'].strip('/') + "/entries"
					photos_path = path_obj['path'].strip('/') + "/photos"

					req = dapi.request('https://api.dropbox.com/1/metadata/dropbox/' + entries_path ).to_url()
					eres = urllib.urlopen(req).read()
					eres_obj = json.loads( eres )

					if len( filter( lambda item: item['path'].endswith('.doentry'), eres_obj['contents'] ) ) > 0:
						#TODO: Farm out into a background task
						api_call = dapi.request('https://api.dropbox.com/1/shares/dropbox/' + entries_path).to_url()
						api_data = json.loads( urllib.urlopen(api_call).read() )
						entries_share_url = api_data['url']

						api_call = dapi.request('https://api.dropbox.com/1/shares/dropbox/' + journal_path).to_url()
						api_data = json.loads( urllib.urlopen(api_call).read() )
						journal_share_url = api_data['url']

						user_profile.journal_path = journal_path
						user_profile.journal_share_url = journal_share_url
						user_profile.entries_path = entries_path
						user_profile.entries_share_url = entries_share_url
						user_profile.photos_path = photos_path

						user_profile.entries_meta = eres
						user_profile.entries_last_sync = time.time()
						user_profile.save()
						
						return redirect('/edit_profile')
						pass
					metadata = lib.format_json( eres )

			except Exception, e:
				errors = form._errors.setdefault('Journal Path',ErrorList())
				errors.append('Selected journal path is not a valid Day one directory')
				print e
				pass
			pass
	else:
		form = SetupProfile_SelectPath_Form()

	return render( request, 'select_journal.html', {
			'journals' : res_obj, #json.dumps( res_obj, indent=4 )
			'metadata' : metadata,
			'form' : form 
	})
	return HttpResponse('lets setup your profile')
	pass

@login_required(login_url='/')
def view_entries(request):
	entries_json = '{}'
	user_profile = _get_request_user_profile(request)
	user_status = Status.factory(request.user)


	meta_job_id = 0
	# on page refresh, start sync task if its been a while!
	if time.time() - user_profile.entries_last_sync > 24*60*60 or True:
		meta_job = tasks.sync_meta.delay( user_profile )
		meta_job_id = meta_job.id
		# set progress status to true
		user_status.set('meta_refresh_in_progress','True')
		user_status.set('meta_refresh_job_id',meta_job_id)

	return render( request, 'view_entries.html', {
			'user' : request.user,
			'meta_job_id' : meta_job_id
		})

from celery.result import AsyncResult

@login_required(login_url='/')
def entries_refresh(request):
	print 'entry'
	obj = { 
		'done' : 0,
		'html' : 'hellooo'
	}


	user_status = Status.factory(request.user)

	# check progress status
	# if in_progress, then check for result status
	# print 'META_STATUS', meta_refresh_in_progress
	user_posts = Post.objects.filter(user_id=request.user.id)
	posts_sync_complete = [ each for each in user_posts if each.sync_complete==True ]
	posts_sync_pending = [ each for each in user_posts if each.sync_complete==False ]

	if user_status.get('meta_refresh_in_progress').value == 'True':
		meta_job_id = user_status.get('meta_refresh_job_id').value
		# print "JOB_ID", meta_job_id
		if meta_job_id > 0:
			meta_job = AsyncResult(meta_job_id)
			if meta_job.status == 'SUCCESS':
				# print 'OK_SUCCESS'
				user_status.set('meta_refresh_in_progress','False')
				user_status.set('meta_refresh_complete','True')

	# if meta is not being refreshed
	# and pending posts is 0
	if len(posts_sync_pending) == 0 and user_status.get('meta_refresh_in_progress').value != 'True':
		obj['done'] = 1

	obj['html'] = "<br>\n".join([ each.uuid for each in posts_sync_complete])
	# now start spawning all the tasks for fetching individual posts
	# if meta refresh is complete
	# if request.session.get('meta_refresh_complete', False):
	# 	pass

	return HttpResponse(json.dumps(obj));





