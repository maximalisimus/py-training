#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class TDict(object):
	
	__slots__ = '__dict__'
	
	def __init__(self, *args):
		super(TDict, self).__init__()
		self.__g = dict(*args)
	
	def __setitem__(self, key, item):
		if not type(key) in (float, int, str, tuple, frozenset, bool, None):
			raise TypeError('Please, enter the \'key\' in (float, int, str, tuple, bool or frozenset)!')
		self.__g[key] = item

	def __getitem__(self, key):
		return self.__g[key] if self.has_key(key) else None
	
	def get(self, k, v = None):
		return self.__g.get(k, v)
	
	def __repr__(self):
		return self.__g.__str__()

	def __len__(self):
		return len(self.__g)

	def __delitem__(self, key):
		del self.__g[key]

	def clear(self):
		return self.__g.clear()

	def copy(self):
		return self.__g.copy()

	def update(self, *args, **kwargs):
		return self.__g.update(*args, **kwargs)

	def keys(self):
		return self.__g.keys()

	def values(self):
		return self.__g.values()

	def items(self):
		return self.__g.items()

	def pop(self, *args):
		return self.__g.pop(*args)

	def setdefault(self, k, d = None):
		return self.__g.setdefault(k, d)

	def fromkeys(self, iterable, value = None):
		if hasattr(iterable, '__iter__'):
			if not hasattr(value, '__iter__') and type(value) != str:
				for item in iterable:
					self.__g[item] = value
			elif type(value) == str:
				for item in iterable:
					self.__g[item] = value
			else:
				if len(value) >= len(iterable):
					for count in range(len(iterable)):
						self.__g[iterable[count]] = value[count]
				elif len(value) < len(iterable):
					for count in range(len(value)):
						self.__g[iterable[count]] = value[count]			
		return self
	
	def __sortOD(self, od, iskey: bool = True, revers: bool = False):
		def CheckToSTR(on_dict, on_key, on_value, reverse_value):
			if hasattr(on_value,'__iter__') and type(on_value) != str:
				tp = type(on_value)
				on_dict[on_key] = tp(sorted(on_value, reverse = reverse_value))
			else:
				on_dict[on_key] = on_value	
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
		tmp = self.__sortOD(self.__g.copy(), iskey, revers)
		self.__g = tmp.copy()
		return self
	
	def popitem(self):
		return self.__g.popitem()

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
			self.__g = dict(sorted(self.__g.items(), key=lambda i: i[0], reverse=True))
		else:
			self.__g = dict(sorted(self.__g.items(), key=lambda i: str(i[0]), reverse=True))
		return self

	def __str__(self):
		return self.__g.__str__()

	def __cmp__(self, dict_):
		return self.__cmp__(self.__g, dict_)

	def __iter__(self):
		return iter(self.__g)

	def __unicode__(self):
		return unicode(repr(self.__g))
	
	def is_emty(self):
		return len(self.__g) == 0
	
	def __contains__(self, item):
		return item in self.__g
	
	def has_key(self, k):
		return k in self.__g

	def has_value(self, v):
		return v in self.__g.values()
	
	def __has_keys(self, od, i: int = 0, *keys):
		if not keys or not od:
			return False
		for k, v in od.items():
			if len(keys) > i:
				if keys[i] == k:
					if isinstance(v, TDict):
						return self.__has_keys(v, i+1, *keys)
					else:
						return True
		return False
	
	def has_keys(self, *keys):
		return self.__has_keys(self.__g.copy(), 0, *keys)

def main():
	dict = TDict
	a = dict({'options': dict({'align': ('Left', 'Center', 'Right', 'Up', 'Down'), \
				'poDesktop': ('Left', 'Center', 'Right', 'Up', 'Down', 'TopLeft', 'TopRight', 'BottomLeft', 'BottomRight')}), \
				'buttons': ('Ok', 'Cancel', 'Abort', 'Esc')})
	print(type(a))
	print(a)
	print(type(a['options']), a['options'])
	print(type(a['buttons']), a['buttons'])
	a.sort()
	print()
	print(type(a))
	print(a)
	print(type(a['options']), a['options'])
	print(type(a['buttons']), a['buttons'])
	print()
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

