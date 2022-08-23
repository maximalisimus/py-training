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

class Border(NoValue):
	LeftTop = '┌'
	RightTop = '┐'
	Vertical = '│'
	Middle = '─'
	LeftBottom = '└'
	RightBottom = '┘'

class fcolor(NoValue):
	''' Foreground Colors '''
	ENDC = '\033[0m'
	HEADER = '\033[95m'
	UNDERLINE = '\033[4m'
	BOLD = '\033[1m'
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

def Border_Text(onText: str, BGColor:FullColor = FullColor(16), BDColor: fcolor = fcolor.White, TxtColor: fcolor = fcolor.White) -> str:
	tmp_text = ''
	count_text = len(onText)
	top_text = BDColor.value + BGColor.FColor + Border.LeftTop() + Border.Middle()*(count_text+2) + Border.RightTop() + BGColor.ENDC + fcolor.ENDC.value
	middle_text = BDColor.value + BGColor.FColor + Border.Vertical() + ' ' + BGColor.ENDC + TxtColor.value + BGColor.FColor + onText + BGColor.ENDC + BDColor.value+ BGColor.FColor + ' ' + Border.Vertical() + BGColor.ENDC + fcolor.ENDC.value
	bottom_text =BDColor.value + BGColor.FColor + Border.LeftBottom() + Border.Middle()*(count_text+2) + Border.RightBottom() + BGColor.ENDC + fcolor.ENDC.value
	return [top_text, middle_text, bottom_text]

def main():
	mycolor = FullColor(19)
	btn1 = Border_Text('OK', mycolor, fcolor.Red, fcolor.LightGreen)
	btn2 = Border_Text('Cancel')
	btn3 = Border_Text('Abort')
	bg = FullColor(19)
	buttons = f"{btn3[0]}{mycolor.FColor} {mycolor.ENDC}{btn1[0]}{mycolor.FColor} {mycolor.ENDC}{btn2[0]}\n{btn3[1]}{mycolor.FColor} {mycolor.ENDC}{btn1[1]}{mycolor.FColor} {mycolor.ENDC}{btn2[1]}\n{btn3[2]}{mycolor.FColor} {mycolor.ENDC}{btn1[2]}{mycolor.FColor} {mycolor.ENDC}{btn2[2]}"
	print(buttons)

if __name__ == '__main__':
	main()
