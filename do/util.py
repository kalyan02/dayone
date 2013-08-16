# import oauth2, json, urlparse, urllib, time, os, plistlib, datetime
from time import mktime
import json, time, datetime, plistlib

class DatetimeTolerantJSONEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, datetime.datetime):
			return int(mktime(obj.timetuple()))

		return json.JSONEncoder.default(self, obj)


def clean_keys(_dict):
	if type(_dict) is dict or type(_dict) is plistlib._InternalDict:
		for key in _dict.keys():
			new_key = key.lower().replace(' ','_')
			_dict[new_key] = _dict[key]
			del _dict[key]
			clean_keys(_dict[new_key])

def json_dumps(obj):
	return json.dumps(obj,cls=DatetimeTolerantJSONEncoder)
