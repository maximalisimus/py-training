#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Integer:
	
	__slots__ = '__dict__'
	
	@classmethod
	def verify_data(cls, value: int):
		if type(value) != int:
			raise TypeError('Enter the line!')
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return getattr(instance, self.name)

	def __set__(self, instance, value: int):
		self.verify_data(value)
		setattr(instance, self.name, value)

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
	def inc(self):
		self.count+=1
		return self
	def dec(self):
		self.count-=1
		return self

class Main(Counter):
	
	__slots__ = 'count'
	
	def __init__(self, start: int = 0):
		super(Main, self).__init__(start)

def main():
	print('Integer() SLOTS:\n',Integer.__slots__, '\n')
	print('Integer() DICT:\n',Integer.__dict__, '\n')
	print('Counter() SLOTS:\n',Counter.__slots__, '\n')
	print('Main() SLOTS:\n',Main.__slots__, '\n')
	c = Main()
	c().inc().inc().dec()
	c(-1).inc().inc().dec()
	c(2).dec().dec()
	print(c)
	print(str(c.count))

if __name__ == '__main__':
	main()
