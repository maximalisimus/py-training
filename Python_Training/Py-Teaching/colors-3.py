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

class ModeTextOut(NoValue):
	Normal = 0 # Grey
	Lighter = 1 # Bold
	Darker = 2
	Italic = 3
	Underline = 4
	BlinkSlow = 5
	BlinkFast = 6
	Inverting = 7
	Hide = 8
	CrossOut = 9

class BiColorInteger:
	''' BiColor class to control setup color value from 16 to 255 '''

	@classmethod
	def verify_int(cls, value: int):
		''' Checking the string data type. '''
		if type(value) != int:
			raise TypeError('Enter the integer!')

	def __set_name__(self, owner, name):
		''' Setting the variable name with 
		two underscores at the beginning of this line. '''
		self.name = "__" + name

	def __get__(self, instance, owner):
		''' Getter of the variable. '''
		return getattr(instance, self.name)

	def __set__(self, instance, value: int):
		''' Variable setter. '''
		self.verify_int(value)
		if (value < 16 or value > 255):
			raise ValueError('Please enter a number between 16 and 255.')
		else:
			setattr(instance, self.name, value)

	def __str__(self):
		''' When referring to a variable as a string, return the value of the variable '''
		return f"{self.value}"

	def __call__(self):
		''' Returning the value of a variable when referring to it as a function '''
		return f"{self.value}"

class BiColor(object):
	BGColor = BiColorInteger()
	FGColor = BiColorInteger()

	def __init__(self, BGColor: int = 16, FGColor: int = 255):
		self.BGColor = BGColor
		self.FGColor = FGColor
	
	def __repr__(self):
		''' Debugging information when calling the class, not printing to the console '''
		return f"{self.__class__}: ({self.BGColor}, {self.FGColor})"

	def __getattribute__(self, name):
		return object.__getattribute__(self, name)

	def __setattr__(self, key, value: int):
		object.__setattr__(self, key, value)

class FullBiColor(object):
	''' The class on FullBiColor 
	
		Modes - ModeTextOut. The Text is output mode: normal, bold, blink, invert, underline, hide
		TextColor - Full text output color: background and foreground
		BGCOLOR - string value background color
		FGCOLOR - string value foreground color
		ENDC - fine color all string
	'''
	BGCOLOR = BiColorInteger()
	FGCOLOR = BiColorInteger()

	def __init__(self, Modes: ModeTextOut = ModeTextOut.Normal, TextColor: BiColor = BiColor(16, 255)):
		self.Modes = Modes
		self.BGCOLOR = TextColor.BGColor
		self.FGCOLOR = TextColor.FGColor
		self.__ENDC = '\x1b[0m'

	@property
	def ENDC(self) -> str:
		return self.__ENDC

	@ENDC.deleter
	def ENDC(self):
		del self.__ENDC

	def getInfo(self):
		return f"{self.__class__}: (ModeTextOut({self.Modes.name}), {self.BGCOLOR}, {self.FGCOLOR})"

	def __repr__(self):
		''' Debugging information when calling the class, not printing to the console '''
		return f"{self.__class__}: (ModeTextOut({self.Modes.name}), {self.BGCOLOR}, {self.FGCOLOR})"
	
	def __getattribute__(self, name):
		return object.__getattribute__(self, name)

	def __str__(self):
		''' When referring to a variable as a string, return the value of the variable '''
		return f"{self.getFGColor}{self.getBGColor}"

	def __call__(self):
		''' Returning the value of a variable when referring to it as a function '''
		return f"{self.getFGColor}{self.getBGColor}"

def main():
	bcolor = BiColor(45, 207)
	print(bcolor)
	mycolor = FullBiColor(ModeTextOut.Lighter, bcolor)
	print(mycolor.getInfo())

if __name__ == '__main__':
	main()
