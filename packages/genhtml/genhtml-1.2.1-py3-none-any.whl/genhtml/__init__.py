class CloseError(OSError):
	pass
class AlreadyClosedError(CloseError):
	pass
class IsClosedError(CloseError):
	pass
class _Tag:
	def __init__(self,tag,**attrs):
		self.tag=tag
		self.attrs=attrs
		self.content=''
		self.closed=False
	def clear_content(self):
		self.content=''
	def write(self,content):
		if not self.closed:
			self.content+=content
		else:
			attrstr=' '
			for i in self.attrs:
				attrstr+=i+'="'+self.attrs[i]+'" '
			attrstr=attrstr.rstrip()
			raise IsClosedError('<'+self.tag+attrstr+'> is closed')
	def close(self):
		if not self.closed:
			self.closed=True
		else:
			attrstr=' '
			for i in self.attrs:
				attrstr+=i+'="'+self.attrs[i]+'" '
			attrstr=attrstr.rstrip()
			raise AlreadyClosedError('already closed <'+self.tag+attrstr+'>')
	def _out(self):
		attrstr=' '
		for i in self.attrs:
			attrstr+=i+'="'+self.attrs[i]+'" '
		attrstr=attrstr.rstrip()
		return '<'+self.tag+attrstr+'>'+self.content+'</'+self.tag+'>'
class HTML(_Tag):
	def __init__(self,intag='html'):
		super(HTML,self).__init__(intag)
		self._alltags=[]
	def open(self,tag):
		return HTML(intag=tag)
	def commit(self,tag):
		self.content+=tag._out()
		self._alltags+=[tag]
	def output(self):
		return self._out()
	@property
	def data_link(self):
		return f'data:text/html,{self.output()}'
	def open_in_browser(self):
		import webbrowser as _wbr
		_wbr.open(f'data:text/html,{self.output()}')
	def get_tags(self):
		return self._alltags
	def set_tags(self,taglist):
		self.content=''
		for i in taglist:
			if isinstance(i,HTML):
				self.content+=i._out()
			elif isinstance(i,str):
				self.content+=i
def formated(html):
	from bs4 import BeautifulSoup
	soup=BeautifulSoup(html, 'lxml')
	return soup.prettify()
