from django import http
from django.utils.http import urlquote
from django.core import urlresolvers
 
 
class AppendOrRemoveSlashMiddleware(object):
	"""
	Like django's built in APPEND_SLASH functionality, but also works in reverse. Eg
	will remove the slash if a slash-appended url won't resolve, but its non-slashed
	counterpart will.
 
	See http://gregbrown.co.nz/code/append-or-remove-slash/ for more information.
	"""
 
	def process_request(self, request):
		"""
		Returns a redirect if adding/removing a slash is appropriate. 
		"""
		
		# check if the url is valid
		urlconf = getattr(request, 'urlconf', None)
		
		if not _is_valid_path(request.path_info, urlconf):
			# if not, check if adding/removing the trailing slash helps
			if request.path_info.endswith('/'):
				new_path = request.path_info[:-1]
			else:
				new_path = request.path_info + '/'
			
			if _is_valid_path(new_path, urlconf):
				# if the new url is valid, redirect to it
				if request.get_host():
					new_url = "%s://%s%s" % (request.is_secure() and 'https' or 'http', request.get_host(), urlquote(new_path))
				else:
					new_url = urlquote(new_path)
				if request.GET:
					new_url += '?' + request.META['QUERY_STRING']
				return http.HttpResponsePermanentRedirect(new_url)
 
			
		
def _is_valid_path(path, urlconf=None):
	"""
	Returns True if the given path resolves against the default URL resolver,
	False otherwise.
	"""
	try:
		urlresolvers.resolve(path, urlconf)
		return True
	except urlresolvers.Resolver404:
		return False