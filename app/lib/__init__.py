import re
from unicodedata import normalize

def slug(text, delim=u'-'):
	"""Generates an slightly worse ASCII-only slug."""
	_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
	result = []
	for word in _punct_re.split(text.lower()):
		word = normalize('NFKD', unicode(word)).encode('ascii', 'ignore')
		if word:
			result.append(word)
	return unicode(delim.join(result))

def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False
	except TypeError:
		return False