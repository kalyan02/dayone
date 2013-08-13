from BeautifulSoup import BeautifulSoup as Soupify
import urllib, re
import settings

import oauth2, urlparse, json
from do import settings


class DropboxAPI(object):
	def __init__(self, user):
		self.user = user
		dinfo = self.user.social_auth.get(provider='dropbox')
		access_token = urlparse.parse_qs( dinfo.extra_data['access_token'] )
		self.user_token = oauth2.Token(key=access_token['oauth_token'][0],secret=access_token['oauth_token_secret'][0])
		self.cons_token = oauth2.Consumer(key=settings.DROPBOX_APP_ID,secret=settings.DROPBOX_API_SECRET)

	def request( self, api_call, extra_params=None ):
		self.parameters = {
	        'oauth_signature_method': oauth2.SignatureMethod_PLAINTEXT.name,
	        'oauth_timestamp'       : oauth2.generate_timestamp(),
	        'oauth_nonce'           : oauth2.generate_nonce(),
	        'oauth_version'         : '1.0',
		}
		if type(extra_params) is dict:
			self.parameters.update(extra_params)

		self.req = oauth2.Request( url=api_call, parameters=self.parameters )
		self.req.sign_request( signature_method=oauth2.SignatureMethod_PLAINTEXT(), token=self.user_token, consumer=self.cons_token)
		return self.req

	def call(self,method,params):
		pass
	

def format_json(json_string):
	return json.dumps( json.loads( json_string ), indent=4 )

# def file_put_contents( fname, fcon ):
# 	fh = open( fname, 'w+' )
# 	fh.write( fcon )
# 	fh.close()

# def file_get_contents( fname ):
# 	fh = open( fname, 'r')
# 	return fh.read()

# dropbox_url = "https://www.dropbox.com/sh/7gcfvmk9h107ryc/F39GaH7W8C"
# con = urllib.urlopen( dropbox_url ).read()
# file_put_contents( 'fh.txt', con )

# con = file_get_contents('fh.txt')
# scon = Soupify( con )
# entries_url = scon.findAll( 'a', attrs={'href':re.compile('/entries$')} )[0]['href']
# photos_url = scon.findAll( 'a', attrs={'href':re.compile('/photos$')} )[0]['href']

# print entries_url
# print photos_url

# # entries_page = urllib.urlopen(entries_url).read()
# # file_put_contents('entries_page.txt',entries_page)
# entries_page = file_get_contents('entries_page.txt')
# econ = Soupify(entries_page)

# posts = econ.findAll( 'a', attrs={'href':re.compile('\.doentry')} )
# urls = [ each['href'] for i,each in enumerate(posts) if i % 2 == 1 ]
# mods = econ.findAll( attrs={'class':'modified-time'} )