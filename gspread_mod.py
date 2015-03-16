import gspread
from gspread.urls import construct_url
from xml.etree import ElementTree

try:
	from urllib import urlencode
except ImportError:
	from urllib.parse import urlencode

class Client(gspread.Client):
	def get_cells_feed(self, worksheet, visibility='private', projection='full', params=None):

		url = construct_url('cells', worksheet,
							visibility='public', projection=projection)

		if params:
			params = urlencode(params)
			url = '%s?%s' % (url, params)

		r = self.session.get(url)
		return ElementTree.fromstring(r.read())