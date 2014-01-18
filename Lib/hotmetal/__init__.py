# -*- coding: utf-8 -*-

from html import *
import types

#from BeautifulSoup import BeautifulSoup


class Text:
	def __init__(self, parent, html):
		self.parent = parent
		self.html = html
	def GenerateHTML(self):
		return self.html

def smart_unicode(s, encoding='utf-8', errors='strict'):
	if type(s) in (unicode, int, long, float, types.NoneType):
		return unicode(s)
	elif type(s) is str or hasattr(s, '__unicode__'):
		return unicode(s, encoding, errors)
	else:
		return unicode(str(s), encoding, errors)

class HotMetalBase:

	# CONSTANTS
	DOCTYPES = {
		'html5': ('<!DOCTYPE html>', 'text/html'),
		'transitional': ('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">', 'text/html'),
		'strict': ('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">', 'text/html'),
		'frameset': ('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd">', 'text/html'),
		'transitionalXHTML': ('<?xml version="1.0" ?>\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">', 'application/xhtml+xml'),
		'strictXHTML': ('<?xml version="1.0" ?>\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">', 'application/xhtml+xml'),
		'framesetXHTML': ('<?xml version="1.0" ?>\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">', 'application/xhtml+xml'),
		'XHTML1.1': ('<?xml version="1.1" ?>\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">', 'application/xhtml+xml'),
		}


	def __init__(self, environment = None, title = None, doctype = 'html5', charset = 'utf-8', besuperstrict = True):

		self.environment = environment
		self.runningID = 0
		self.warnings = []
		self.besuperstrict = besuperstrict # Set whether HTML tag attributes of wrong type should be exported anyway, and mimetype
		
		# HEAD
		self.doctype = doctype
		self.doctypetag = self.DOCTYPES[doctype][0]
		self.mimetype = self.DOCTYPES[doctype][1]
		if not self.besuperstrict:
			self.mimetype = 'text/html'
		self.charset = charset
		self.contenttype = "%s; charset=%s" % (self.mimetype, self.charset)
		self.title = title
		self.headtags = []
		self.bodytags = []
		self.headscript = []
		self.css = {}
		
#		self.META(http_equiv = 'Content-Type', content='%s; charset=%s' % (self.mimetype, self.charset))
		self.META(http_equiv = 'Content-Type', content=self.contenttype)
	
		self.initialize()

	def initialize(self):
		pass

	def RunningID(self):
		u"""\
		Just a number being incremented.
		"""
		self.runningID += 1
		return self.runningID

	def Warning(self, string):
		u"""\
		Issue a warning.
		"""
		self.warnings.append(string)

	def OutputWarnings(self, glue = '\n'):
		u"""\
		Output Warnings for debugging.
		"""
		return glue.join(map(str, self.warnings))
		
	
	# HEAD TAGS

	def RSSLink(self, target):
		self.LINK(rel='alternate', type='application/rss+xml', title='RSS', href=target)

	def CSSLink(self, target, media = None):
		self.LINK(rel='stylesheet', type='text/css', href=target, media=media)
	
	def JSLink(self, target):
		self.HeadT('<script src="%s" type="text/javascript"></script>' % (target))

	def HeadScript(self, text):
		self.headscript.append(text)

	# META TAGS
	def CSS(self, selector, key, value):
		if not self.css.has_key(selector):
			self.css[selector] = {}
		self.css[selector][key] = value

	def CheckBox(self, id = None, class_ = None, onclick = None, text = None, checked = False):
		if not id:
			id = "%s_checkbox" % (self.RunningID())

		self.INPUT(type='checkbox', id = id, onclick = onclick, class_ = class_, checked=checked)
		self.T(' ')
		self.SPAN(class_ = class_, onclick="document.getElementById('%s').click()" % id, style='cursor:default')
		self.T(text)
		self._SPAN()

	def T(self, html = None):
		self.bodytags.append(Text(self, html))

	def HeadT(self, html = None):
		self.headtags.append(Text(self, html))


	# OUTPUT

	def GenerateBody(self, glue = u''):
		html = []

		for tag in self.bodytags:
			html.append(tag.GenerateHTML())

#		soup = BeautifulSoup(glue.join(map(str,html)))
#		good_html = soup.prettify()
#		return good_html
		return glue.join(map(smart_unicode, html))


	def GeneratePage(self, glue = u''):
		string = []

		# HEAD
		string.append(self.doctypetag)
		if "XHTML" in self.doctype:
			string.append('<html xmlns="http://www.w3.org/1999/xhtml">')
		else:
			string.append("<html>")
		string.append("<head>")
		if self.title:
			string.append("<title>%s</title>" % (self.title))

		for item in self.headtags:
			string.append(item.GenerateHTML())

		if self.headscript:
			string.append('<script type="text/javascript">')
			headscriptlines = []
			for item in self.headscript:
				headscriptlines.append(item)
			string.append('\n'.join(map(str,headscriptlines)))
			string.append('</script>')

		if self.css:
			string.append('<style type="text/css">')
			for css in self.css:
				string.append('%s {\n' % (css))
				for key in self.css[css]:
					string.append('%s: %s;\n' % (key, self.css[css][key]))
				string.append('}\n')
			string.append('</style>')

		string.append("</head>")

		# BODY
		string.append("<body>")
		string.append(self.GenerateBody(glue))
		string.append("</body>")

		string.append("</html>")

#		soup = BeautifulSoup(glue.join(map(str,string)))
#		good_html = soup.prettify()
#		return good_html
#		return glue.join(map(str,string))
		return glue.join(map(smart_unicode, string))


class BaseHTMLTag:
	
	def DocTypeAllowed(self, alloweddoctypes):
		DocTypeAllowed = False
		
		for doctype in alloweddoctypes.split(','):
			if doctype in self.parent.doctype or 'html5' in self.parent.doctype:
				DocTypeAllowed = True
		return DocTypeAllowed
		
	
	def HtmlVarTypeCDATA(self, alloweddoctypes, attribute, string):
		if string != None:
			if self.DocTypeAllowed(alloweddoctypes):
				try:
					#a = str(string)
					return string.encode(self.parent.charset)
				except:
					self.parent.Warning("Attribute %s could not be converted to string for tag &lt;%s&gt; and charset %s." % (attribute, self.tag, self.parent.charset))
					if not self.parent.besuperstrict:
						return string
			else:
				self.parent.Warning("Attribute %s is only allowed for doctypes %s for tag &lt;%s&gt;." % (attribute, alloweddoctypes, self.tag))
				if not self.parent.besuperstrict:
					return string

	def HtmlVarTypeINT(self, alloweddoctypes, attribute, integer):
		if integer != None:
			if self.DocTypeAllowed(alloweddoctypes):
				try:
					a = int(integer)
					return integer
				except:
					self.parent.Warning("Attribute %s (%s) could not be converted to integer for tag &lt;%s&gt;." % (attribute, integer, self.tag))
					if not self.parent.besuperstrict:
						return integer
			else:
				self.parent.Warning("Attribute %s is only allowed for doctypes %s for tag &lt;%s&gt;." % (attribute, alloweddoctypes, self.tag))
				if not self.parent.besuperstrict:
					return integer

	def HtmlVarTypeID(self, alloweddoctypes, attribute, string):
		if string != None:
			if self.DocTypeAllowed(alloweddoctypes):
				try:
					a = str(string)
					ForbiddenCharacterFound = False
					for c in string:
						if not c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_:.':
							ForbiddenCharacterFound = True
					if ForbiddenCharacterFound:
						self.parent.Warning("Attribute %s of type ID contains illegal character(s) (%s) for for tag &lt;%s&gt;." % (attribute, c, self.tag))
						if not self.parent.besuperstrict:
							return string
					if string[0:1] in '-_:.':
						self.parent.Warning("Attribute %s of type ID starts with illegal character (%s) for for tag &lt;%s&gt;." % (attribute, string, self.tag))
						if not self.parent.besuperstrict:
							return string
				except:
					self.parent.Warning("Attribute %s could not be converted to string for tag &lt;%s&gt;." % (attribute, self.tag))
					if not self.parent.besuperstrict:
						return string
			else:
				self.parent.Warning("Attribute %s is only allowed for doctypes %s for tag &lt;%s&gt;." % (attribute, alloweddoctypes, self.tag))
				if not self.parent.besuperstrict:
					return string

	def HtmlVarTypeFixedList(self, alloweddoctypes, attribute, string, fixedlist):
		if string != None:
			if self.DocTypeAllowed(alloweddoctypes):
				if string in fixedlist:
					return string
				else:
					self.parent.Warning("Attribute %s (%s) is not of valid choices (%s) for tag &lt;%s&gt;." % (attribute, string, ', '.join(map(str, fixedlist)), self.tag))
					if not self.parent.besuperstrict:
						return string
			else:
				self.parent.Warning("Attribute %s is only allowed for doctypes %s for tag &lt;%s&gt;." % (attribute, alloweddoctypes, self.tag))
				if not self.parent.besuperstrict:
					return string


	def HtmlVarTypeEmpty(self, alloweddoctypes, attribute, var):
		if var:
			return '__//empty//__'

	def AddUniversalAttributes(self, class_, id, style, title, dir, lang, onclick, ondblclick, onmousedown, onmouseup, onmouseover, onmousemove, onmouseout, onkeypress, onkeydown, onkeyup):
		# Universal Attributes
		self.attributes['class'] = self.HtmlVarTypeCDATA('strict,transitional,framset', 'class', class_)
		self.attributes['id'] = self.HtmlVarTypeCDATA('strict,transitional,framset', 'id', id)
		self.attributes['style'] = self.HtmlVarTypeCDATA('strict,transitional,framset', 'style', style)
		self.attributes['title'] = self.HtmlVarTypeCDATA('strict,transitional,framset', 'title', title)
		self.attributes['dir'] = self.HtmlVarTypeCDATA('strict,transitional,framset', 'dir', dir)
		self.attributes['lang'] = self.HtmlVarTypeCDATA('strict,transitional,framset', 'lang', lang)
		self.attributes['onclick'] = self.HtmlVarTypeCDATA('strict,transitional,framset', 'onclick', onclick)
		self.attributes['ondblclick'] = self.HtmlVarTypeCDATA('strict,transitional,framset', 'ondblclick', ondblclick)
		self.attributes['onmousedown'] = self.HtmlVarTypeCDATA('strict,transitional,framset', 'onmousedown', onmousedown)
		self.attributes['onmouseup'] = self.HtmlVarTypeCDATA('strict,transitional,framset', 'onmouseup', onmouseup)
		self.attributes['onmouseover'] = self.HtmlVarTypeCDATA('strict,transitional,framset', 'onmouseover', onmouseover)
		self.attributes['onmousemove'] = self.HtmlVarTypeCDATA('strict,transitional,framset', 'onmousemove', onmousemove)
		self.attributes['onmouseout'] = self.HtmlVarTypeCDATA('strict,transitional,framset', 'onmouseout', onmouseout)
		self.attributes['onkeypress'] = self.HtmlVarTypeCDATA('strict,transitional,framset', 'onkeypress', onkeypress)
		self.attributes['onkeydown'] = self.HtmlVarTypeCDATA('strict,transitional,framset', 'onkeydown', onkeydown)
		self.attributes['onkeyup'] = self.HtmlVarTypeCDATA('strict,transitional,framset', 'onkeyup', onkeyup)

	def GenerateHTML(self):
		html = []
		# tag name
		html.append(self.tag)
		# Attributes
		for attr in self.attributes:
			if self.attributes.has_key(attr):
				if self.attributes[attr] == '__//empty//__':
					html.append('%s' % (attr))
				elif self.attributes[attr]:
					html.append('%s="%s"' % (attr, self.attributes[attr]))
		if self.singletag and 'XHTML' in self.parent.doctype:
			html.append('/')

		return '<%s>' % (" ".join(map(str,html)).strip())


class BaseHTMLClosingTag:
	def GenerateHTML(self):
		return '</%s>' % (self.tag)
