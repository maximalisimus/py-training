#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Integer:
	
	__slots__ = '__dict__', '__weakref__'
	
	@classmethod
	def verify_data(cls, value: int):
		if type(value) != int:
			raise TypeError('Enter the line!')
	
	def __init__(self, value: int = 0):
		self.value = value
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return getattr(instance, self.name)

	def __set__(self, instance, value: int):
		self.verify_data(value)
		setattr(instance, self.name, value)

	def __del__(self):
		# Debug
		# print('Integer delete.')
		del self

class Calc(object):
	
	__slots__ = ()
	
	def inc(self):
		self.count+=1
		return self

	def dec(self):
		self.count-=1
		return self

	def __del__(self):
		# Debug
		# print('Calc delete.')
		del self

class Info(object):
	
	@property
	def value(self):
		return f"{self.count}"

class Counter(object):
	
	__slots__ = ()
	
	count = Integer()
	
	def __init__(self, start: int = 0):
		self.count = start

	def __call__(self, orient: int = 1):
		self.count+=orient
		return self

	def __repr__(self):
		return f"{self.__class__}: {self.count}"

	def __str__(self):
		return f"{self.count}"

	def __del__(self):
		# Debug
		# print('Counter delete.')
		del self

class Main(Calc, Counter, Info):
	
	__slots__ = 'count'
	# Example
	#__slots__ = 'count a b'.split()
	
	def __init__(self, start: int = 0):
		super(Main, self).__init__(start)
		# Example
		#self.a = self.count
		#self.b = self.count

	def __del__(self):
		# Debug
		# print('Main delete.')
		del self

def main():
	c = Main()
	c().inc().dec()
	print(f"{c.__class__}: {dir(c)}")
	print(c.value)
	del c

if __name__ == '__main__':
	main()
