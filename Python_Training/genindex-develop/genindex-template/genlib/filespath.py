__all__ = 'Line PathString FMode FExt FExts FSize Boolean Integer Files Icon'.split()

import pathlib
import base64
from stat import filemode
import sys

from .datestamp import *
from .default import size_format, default_file, default_template

class Line:
	
	@classmethod
	def verify_str(cls, value):
		if type(value) != str:
			raise TypeError('Enter the string!')

	def __set_name__(self, owner, name):
		self.name = "__" + name

	def __get__(self, instance, owner):
		return getattr(instance, self.name)

	def __set__(self, instance, value):
		self.verify_str(value)
		setattr(instance, self.name, value)

class PathString:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name

	def __get__(self, instance, owner):
		return getattr(instance, self.name)

	def __set__(self, instance, value: str):
		setattr(instance, self.name, pathlib.Path(f"{value}").resolve())

class FMode:
	
	def __set_name__(self, owner, name):
		self.name = "file"

	def __get__(self, instance, owner):
		value = getattr(instance, self.name)
		return f"{filemode(value.stat().st_mode)}" if value.exists() else '----------'

class FExt:
	
	def __set_name__(self, owner, name):
		self.name = "file"

	def __get__(self, instance, owner):
		value = getattr(instance, self.name)
		return str(value.suffix).replace('.', '')

class FExts:
	
	def __set_name__(self, owner, name):
		self.name = "file"

	def __get__(self, instance, owner):
		value = getattr(instance, self.name)
		return list(map(lambda x: str(x).replace('.', ''), value.suffixes))

class FSize:
	
	def __set_name__(self, owner, name):
		self.name = "file"

	def __get__(self, instance, owner):
		value = getattr(instance, self.name)
		return size_format(value.stat().st_size) if value.exists() else size_format(0)

class Boolean:

	@classmethod
	def verify_bool(cls, value):
		if type(value) != bool:
			raise TypeError('Enter the boolean!')

	def __set_name__(self, owner, name):
		self.name = "__" + name

	def __get__(self, instance, owner):
		return getattr(instance, self.name)

	def __set__(self, instance, value):
		self.verify_bool(value)
		setattr(instance, self.name, value)

class Integer:

	@classmethod
	def verify_bool(cls, value):
		if type(value) != int:
			raise TypeError('Enter the integer!')

	def __set_name__(self, owner, name):
		self.name = "__" + name

	def __get__(self, instance, owner):
		return getattr(instance, self.name)

	def __set__(self, instance, value):
		self.verify_bool(value)
		setattr(instance, self.name, value)

class Files:
	
	__slots__ = ['__dict__']
	
	file = PathString()
	strformat = Line()
	mode = FMode()
	ext = FExt()
	exts = FExts()
	size = FSize()
	isjson = Boolean()
	indent = Integer()
	
	def __init__(self, *args, **kwargs):
		self.file = args[0] if len(args) >= 1 else kwargs.get('file', './')
		self.strformat = args[1] if len(args) >= 2 else kwargs.get('strformat', '%d-%b-%Y %H:%M')
		self.isjson = args[2] if len(args) >= 3 else kwargs.get('isjson', False)
		self.indent = args[3] if len(args) >= 4 else kwargs.get('indent', 2)
	
	def __str__(self):
		return f"{self.file}"
	
	def __repr__(self):
		''' For Debug Function output paramters. '''
		except_list = ['date', 'join', 'unjoin', 'read', 'write', 'writeBase64', 'readBase64', 'tobase64', 'totext']
		return f"{self.__class__}:\n\t" + \
				'\n\t'.join(f"{x}: {getattr(self, x)}" for x in dir(self) if not x in except_list and '__' not in x)
	
	@property
	def date(self):
		return stampToStr(self.file.stat().st_mtime, self.strformat) if self.file.exists() else '12-Aug-1981 00:00'
	
	def join(self, path):
		self.file = str(self.file.joinpath(str(path)))
		return self
	
	def unjoin(self):
		self.file = str(self.file.parent)
		return self
	
	def read(self):
		if self.file.exists():
			with open(self.file, 'r') as fp:
				if self.isjson:
					return json.load(fp)
				else:
					return fp.read()
	
	def write(self, data = '', typerw: str = 'w'):
		typerw = typerw.replace('+','').replace('r','w')
		with open(self.file, typerw) as fp:
			if self.isjson:
				if not 'b' in typerw and not 'r' in typerw:
					json.dump(data, fp, indent=self.indent)
			else:
				fp.write(data)
	
	def writeBase64(self, data64 = '', typerw: str = 'wb', coding = 'ascii'): # utf-8
		typerw = typerw.replace('+','').replace('r','w')
		with open(self.file, typerw) as file:
			file.write(self.totext(data64, True, coding)) if 'b' in typerw else file.write(self.totext(data64, False, coding))
	
	def readBase64(self, typerw: str = 'rb', coding = 'ascii'): # utf-8
		typerw = typerw.replace('+','').replace('a','r').replace('w','r')
		if self.file.exists():
			with open(self.file, typerw) as file:
				data = file.read()
			return self.tobase64(data, True, coding) if 'b' in typerw else self.tobase64(data, False, coding)
	
	@classmethod
	def tobase64(cls, text, isbyte: bool = False, coding = 'ascii'): # utf-8
		return base64.b64encode(text).decode(coding) if isbyte else base64.b64encode(text.encode(coding)).decode(coding)
	
	@classmethod
	def totext(cls, text64, isbyte: bool = False, coding = 'ascii'): # utf-8
		return base64.b64decode(text64.encode(coding)) if isbyte else base64.b64decode(text64.encode(coding)).decode(coding)

class Icon:
	
	__slots__ = ['__dict__']
	
	name = Line()
	template = Line()
	
	def __init__(self, *args, **kwargs):
		self.name = args[0] if len(args) >= 1 else kwargs.get('name', 'file')
		self.template = args[1] if len(args) >= 2 else kwargs.get('template', default_template)
	
	def __str__(self):
		return f"{self.name}"
	
	def __repr__(self):
		''' For Debug Function output paramters. '''
		except_list = ['getFile']
		return f"{self.__class__}:\n\t" + \
				'\n\t'.join(f"{x}: {getattr(self, x)}" for x in dir(self) if not x in except_list and '__' not in x)
	
	@property
	def getFile(self):
		tempfile = list(filter(lambda x: self.template in str(x), sorted(pathlib.Path(sys.argv[0]).parent.rglob(f"{self.name}.png"))))[0]
		return str(tempfile.resolve() if str(tempfile) != '' else default_file)
	
