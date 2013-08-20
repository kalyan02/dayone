from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.http import HttpResponse, Http404
from django.forms import models, ModelForm, HiddenInput
from do.models import *
from django.db import connection
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django import forms
from django.forms.util import ErrorList
from django.template.loader import render_to_string

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import oauth2, json, urlparse, urllib, time, os, plistlib, datetime, re
from time import mktime
from do import settings, lib, tasks, util
import markdown


def _get_content(post):
	content = json.loads(post.content)
	content['id'] = post.id
	content['json'] = "<pre>%s</pre>" % json.dumps(content,indent=4)
	content['entry_text'] = re.sub( '(#(\w+))', r'<a href="#">\#\2</a>',content['entry_text'] )
	content['entry_text'] = content['entry_text'].replace("\n", "    \n");
	content['entry_html'] = markdown.markdown(content['entry_text'])

	content['creation_date'] = datetime.datetime.fromtimestamp( int(content['creation_date']) ).strftime('%a, %b %d, %Y')
	return content


def dayroll(request):
	the_page = request.GET.get('page')
	user_posts = Post.objects.filter( Q(is_public=True) | Q(is_anonymous=True) ).order_by('-id')
	paginator = Paginator( user_posts, 10 )

	try:
		page_posts = paginator.page(the_page)
	except PageNotAnInteger:
		page_posts = paginator.page(1)
	except EmptyPage:
		page_posts = paginator.page(paginator.num_pages)


	# fleshen the content of the objects we require in the page
	all_posts = []
	for page_post in page_posts.object_list:
		all_posts.append( _get_content(page_post) )
	# and assign it back to the pagination post object - it makes life easier
	page_posts.object_list = all_posts

	return render( request, 'dayroll.html', {
			'user' : request.user,
			'all_posts' : page_posts
		})

def daypost(request, post_id):
	try:
		user_post = Post.objects.get( id=post_id )
	except:
		raise Http404

	if not user_post:
		raise Http404

	if not user_post.is_public and not user_post.is_anonymous:
		return page_404(request)
		raise Http404



	return render( request, 'daypost.html', {
			'user' : request.user,
			'post' : _get_content(user_post)
		})

def page_404(request):
    # response = render_to_response('404.html', locals(), context_instance=RequestContext(request))
	# return HttpResponse('shit')
	# return HttpResponse('shit',status=404)
	return render( request, '404.html', status=404 )

def main(request):
	return redirect('/dayroll')