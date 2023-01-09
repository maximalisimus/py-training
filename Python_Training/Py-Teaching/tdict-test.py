#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class TDict(object):
	
	__slots__ = '__dict__'
	
	def __init__(self, *args):
		super(TDict, self).__init__()
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
	
	def __sortOD(self, od, iskey: bool = True, revers: bool = False):
		def CheckToSTR(on_dict, on_key, on_value, reverse_value):
			if hasattr(on_value,'__iter__') and type(on_value) != str:
				tp = type(on_value)
				on_dict[on_key] = tp(sorted(on_value, reverse = reverse_value))
			else:
				on_dict[on_key] = v		
		res = TDict()
		if not TDict in set(map(type, od.values())):
			if iskey:
				if len(set(map(type,od.keys()))) == 1:
					for k, v in sorted(od.items(), key=lambda i: i[0], reverse = revers):
						CheckToSTR(res, k, v, revers)
				else:
					for k, v in sorted(od.items(), key=lambda i: str(i[0]), reverse = revers):
						CheckToSTR(res, k, v, revers)
			else:
				if len(set(map(type,od.values()))) == 1:
					for k, v in sorted(od.items(), key=lambda i: i[1], reverse = revers):
						CheckToSTR(res, k, v, revers)
				else:
					for k, v in sorted(od.items(), key=lambda i: str(i[1]), reverse = revers):
						CheckToSTR(res, k, v, revers)
		else:
			if len(set(map(type,od.keys()))) == 1:
				for k, v in sorted(od.items(), reverse = revers):
					if isinstance(v, TDict):
						res[k] = self.__sortOD(v)
					else:
						CheckToSTR(res, k, v, revers)
			else:
				for k, v in sorted(od.items(), key=lambda i: str(i[0]), reverse = revers):
					if isinstance(v, TDict):
						res[k] = self.__sortOD(v)
					else:
						CheckToSTR(res, k, v, revers)
		return res
	
	def sort(self, iskey: bool = True, revers: bool = False):
		tmp = self.__sortOD(self.__dict__.copy(), iskey, revers)
		self.__dict__ = tmp.copy()
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
		if len(set(map(type, self.keys()))) == 1:
			self.__dict__ = dict(sorted(self.__dict__.items(), key=lambda i: i[0], reverse=True))
		else:
			self.__dict__ = dict(sorted(self.__dict__.items(), key=lambda i: str(i[0]), reverse=True))
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
	a = [(1, 'True'), (2, 'False'), (3, 'Else')]
	#a = [(1, [1,2,3]), (3, [4,5,6]), (2, [7,8,9])]
	#a = [(1, True), (2, False), (3, None)]
	b = TDict(a)
	#print(b.sort(True, False))
	#print(b.sort(True, True))
	#print(b.sort(False, False))
	#print(b.sort(False, True))
	c = TDict([(3, 'Str'), (4, 'Main')])
	print('b:',b)
	print('c:',c)
	d = b|c
	print()
	print('d = b|c:', d)
	print('d.sort(True, False):',d.sort(True, False))
	print('d.sort(True, True):',d.sort(True, True))
	print('d.sort(False, False):',d.sort(False, False))
	print('d.sort(False, True):',d.sort(False, True))
	print()
	mydict1 = TDict(((1, 'LoL'),(2, 'KeK'),(3, 'Cheburek')))
	mydict2 = TDict(((4, None), (5, None), (6, None)))
	list_dict = TDict()
	list_dict[mydict1] = 0
	list_dict[mydict2] = 0
	print('list_dict:',list_dict)
	print('tuple(list_dict.keys())[0]:',tuple(list_dict.keys())[0])
	print('tuple(list_dict.keys())[1]:',tuple(list_dict.keys())[1])
	print()
	dict_list = TDict()
	dict_list[0] = mydict1
	dict_list[1] = mydict2
	print('dict_list:',dict_list)
	print('tuple(dict_list.values())[0]:',tuple(dict_list.values())[0])
	print('tuple(dict_list.values())[1]:',tuple(dict_list.values())[1])
	print()
	my_list = []
	my_list.append(mydict1)
	my_list.append(mydict2)
	print('my_list:',my_list)
	print('my_list[0]:',my_list[0])
	print('my_list[0]:',my_list[1])

if __name__ == '__main__':
	main()

