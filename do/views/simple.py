from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse

def simple_view_factory(response_str):
	def _fn(_request):
		return HttpResponse(response_str)
	return _fn

# main = simple_view_factory('index')
auth_ok = simple_view_factory('auth is ok')
login_ok = auth_ok

def main(request):
	return render( request, 'main.html', { 'user': request.user } )