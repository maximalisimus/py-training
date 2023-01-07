#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class TDict:
	
	__slots__ = '__dict__'
	
	def __init__(self, *args):
		self.__dict__ = dict(*args)
	
	def __setitem__(self, key, item):
		self.__dict__[key] = item

	def __getitem__(self, key):
		return self.__dict__[key]

	def __repr__(self):
		return f"{self.__class__}"

	def __len__(self):
		return len(self.__dict__)

	def __delitem__(self, key):
		del self.__dict__[key]

	def clear(self):
		return self.__dict__.clear()

	def copy(self):
		return self.__dict__.copy()

	def has_key(self, k):
		return k in self.__dict__

	def has_value(self, v):
		return v in self.__dict__.values()

	def update(self, *args, **kwargs):
		return self.__dict__.update(*args, **kwargs)

	def keys(self):
		return self.__dict__.keys()

	def values(self):
		return self.__dict__.values()

	def items(self):
		return self.__dict__.items()

	def pop(self, *args):
		return self.__dict__.pop(*args)

	def setdefault(self, k, d = None):
		return self.__dict__.setdefault(k, d)

	def fromkeys(self, iterable, value = None):
		if hasattr(iterable, '__iter__'):
			if not hasattr(value, '__iter__'):
				for item in iterable:
					self.__dict__[item] = value
			else:
				if len(value) >= len(iterable):
					for count in range(len(iterable)):
						self.__dict__[iterable[count]] = value[count]
				elif len(value) < len(iterable):
					for count in range(len(value)):
						self.__dict__[iterable[count]] = value[count]
		return self
	
	def sort(self, revers: bool = False):
		self.__dict__ = dict(sorted(self.__dict__.items(), key=lambda i: i[0], reverse = revers))
		return self
	
	def popitem(self):
		return self.__dict__.popitem()

	def __or__(self, other):
		if not isinstance(other, TDict):
			return NotImplemented
		new = TDict(self)
		new.update(other)
		return new

	def __ror__(self, other):
		if not isinstance(other, TDict):
			return NotImplemented
		new = TDict(other)
		new.update(self)
		return new

	def __ior__(self, other):
		TDict.update(self, other)
		return self
	
	def __reversed__(self):
		self.__dict__ = dict(sorted(self.__dict__.items(), key=lambda i: i[0], reverse=True))
		return self

	def __str__(self):
		return self.__dict__.__str__()

	def __cmp__(self, dict_):
		return self.__cmp__(self.__dict__, dict_)

	def __contains__(self, item):
		return item in self.__dict__

	def __iter__(self):
		return iter(self.__dict__)

	def __unicode__(self):
		return unicode(repr(self.__dict__))
	
	def is_emty(self):
		return len(self.__dict__) == 0
	
	def has_values(self, *v):
		if not v:
			return False
		if len(v) == 1:
			return self.has_value(v[0])
		else:
			values = []
			for item in v:
				values.append(self.has_value(item))
			return values
	
	def has_keys(self, *k):
		if not k:
			return False
		if len(k) == 1:
			return self.has_key(k[0])
		else:
			keys = []
			for key in k:
				keys.append(self.has_key(key))

def main():
	a = [(1, True), (2, False), (3, True)]
	b = TDict(a)
	c = TDict([(3, 'Str'), (4, 'Main')])
	print(b)
	print(c)
	d = b|c
	print(d)

if __name__ == '__main__':
	main()

# ['__class_getitem__', '__contains__', '__delitem__', \
# '__getitem__', '__ior__', '__iter__', '__len__', '__or__', \
# '__reversed__', '__ror__', '__setitem__', 'clear', 'copy', \
# 'fromkeys', 'get', 'items', 'keys', 'pop', 'popitem', \
# 'setdefault', 'update', 'values']

