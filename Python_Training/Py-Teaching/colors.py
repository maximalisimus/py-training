#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum

class NoValue(Enum):
	''' Base Enum Class '''

	def __repr__(self):
		''' Debugging information when calling the class, not printing to the console '''
		return f"{self.__class__}: {self.name}"
	
	def __str__(self):
		''' When referring to a variable as a string, return the value of the variable '''
		return f"{self.value}"
	
	def __call__(self):
		''' Returning the value of a variable when referring to it as a function '''
		return f"{self.value}"

class ccolor(NoValue):
	''' Control Colors '''
	ENDC = '\033[0m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	BOLD = '\033[1m'
	HEADER = '\033[95m'
	UNDERLINE = '\033[4m'

class fcolor(NoValue):
	''' Foreground Colors '''
	Black = '\033[0;30m'
	Red = '\033[0;31m'
	Green = '\033[0;32m'
	Orange = '\033[0;33m'
	Blue = '\033[0;34m'
	Purple = '\033[0;35m'
	Cyan = '\033[0;36m'
	LightGray = '\033[0;37m'
	DarkGray = '\033[1;30m'
	LightRed = '\033[1;31m'
	LightGreen = '\033[1;32m'
	Yellow = '\033[1;33m'
	LightBlue = '\033[1;34m'
	LightPurple = '\033[1;35m'
	LightCyan = '\033[1;36m'
	White = '\033[1;37m'

class bcolor(NoValue):
	''' Background Colors '''
	LightGray = '\033[0;40m'
	LightRed = '\033[0;41m'
	LightGreen = '\033[0;42m'
	LightYellow = '\033[0;43m'
	LightBlue = '\033[0;44m'
	LightPurple = '\033[0;45m'
	LightCyan = '\033[0;46m'
	BoldWhite = '\033[0;47m'
	Gray = '\033[1;40m'
	Red = '\033[1;41m'
	Green = '\033[1;42m'
	Yellow = '\033[1;43m'
	Blue = '\033[1;44m'
	Purple = '\033[1;45m'
	Cyan = '\033[1;46m'
	White = '\033[1;47m'

class NoColor:
	''' NoColor class to control setup color value '''
	
	@classmethod
	def verify_str(cls, value: int):
		''' Check value on Type '''
		if type(value) != int:
			raise TypeError('Enter the line!')

	def __set_name__(self, owner, name):
		''' Setup name on variable '''
		self.name = "__" + name

	def __get__(self, instance, owner):
		''' Get the value of a variable '''
		return getattr(instance, self.name)

	def __set__(self, instance, value: int):
		''' Set the value of the variable in the range from 16 to 255 '''
		self.verify_str(value)
		if (value < 16 or value > 255):
			raise ValueError('Please enter a number between 16 and 255.')
		else:
			setattr(instance, self.name, f"\x1b[48;5;{value}m")

	def __str__(self):
		''' When referring to a variable as a string, return the value of the variable '''
		return f"{self.value}"

	def __call__(self):
		''' Returning the value of a variable when referring to it as a function '''
		return f"{self.value}"

class FullColor(object):
	''' FullColor class - a class in which you can set the rgb color like a bash console. '''

	FColor = NoColor()

	def __init__(self, value: int = 16):
		''' Setting the initial color value, if there is one. The END value is a constant. '''
		self.__ENDC = '\x1b[0m'
		self.FColor = value

	@property
	def ENDC(self):
		''' Returning the end of a full color line '''
		return self.__ENDC

def main():
	index = 0
	for item in fcolor:
		print(item, index, end='')
		index+=1
	print(ccolor.ENDC)
	index = 0
	for count in bcolor:
		print(count, index, end='')
		index+=1
	print(ccolor.ENDC)
	index = 0
	for count in bcolor:
		for item in fcolor:
			print(count, item, index, end='')
			index+=1
	print(ccolor.ENDC)
	index = 0
	for count in bcolor:
		for item in fcolor:
			print(ccolor.BOLD, count, item, index, end='')
			index+=1
	print(ccolor.ENDC)
	mycolor = FullColor()
	for i in range(16, 256):
		mycolor.FColor = i
		print(f"{mycolor.FColor}{i}{mycolor.ENDC}", end = ' ')

if __name__ == '__main__':
	main()
