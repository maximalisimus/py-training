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
	
	@classmethod
	def verify_str(cls, value: str):
		if type(value) != str:
			raise TypeError('Enter the string!')

	def __set_name__(self, owner, name):
		self.name = "__" + name

	def __get__(self, instance, owner):
		return getattr(instance, self.name)

	def __set__(self, instance, value: str):
		self.verify_str(value)
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
		except_list = ['join', 'unjoin', 'read', 'write', 'readBase64']
		return f"{self.__class__}:\n\t" + \
				'\n\t'.join(f"{x}: {getattr(self, x)}" for x in dir(self) if not x in except_list and '__' not in x)
	
	@property
	def date(self):
		return stampToStr(self.file.stat().st_mtime, self.strformat) if self.file.exists() else '12-Aug-1981 00:00'
	
	def joinNO(self, path):
		return Files(str(self.file.joinpath(str(path))))
	
	def join(self, path):
		self.file.joinpath(str(path))
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
	
	def write(self, data = '', typerw = 'w'):
		with open(self.file, typerw) as fp:
			if self.isjson:
				json.dump(data, fp, indent=self.indent)
			else:
				fp.write(data)
	
	def readBase64(self):
		if self.file.exists():
			with open(self.file, "rb") as file:
				data = file.read()
			return base64.b64encode(data).decode("ascii")

class Icon(Files):
	
	def __init__(self, *args, **kwargs):
		self.value = args[4] if len(args) >= 5 else kwargs.get('value', 'file')
		self.template = args[5] if len(args) >= 6 else kwargs.get('template', default_template)
		tempfile = list(filter(lambda x: self.template in str(x), sorted(pathlib.Path(sys.argv[0]).parent.rglob(f"{self.value}.png"))))[0]
		super(Icon, self).__init__(file = str(tempfile.resolve() if str(tempfile) != '' else default_file), *args, **kwargs)	
