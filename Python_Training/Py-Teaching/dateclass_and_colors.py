#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum
from dataclasses import dataclass, asdict

class NoValue(Enum):
	''' Base Enum Class '''

	def __repr__(self):
		''' Debugging information when calling the class, not printing to the console '''
		return f"{self.__class__}: {self.name}"

	def __str__(self):
		''' When referring to a variable as a string, return the value of the variable '''
		return f"{self.name}"

	def __call__(self):
		''' Returning the value of a variable when referring to it as a function '''
		return f"{self.value}"

class Border(NoValue):
	LeftTop = '┌'
	RightTop = '┐'
	Middle = '─'
	Vertical = '│'
	LeftBottom = '└'
	RightBottom = '┘'

class EscSeq(NoValue):
	SEP = '\\'
	ESC = 'x1b['
	FINE = 'x1b[0m'
	FGFULL = '38;2;'
	BGFULL = '48;2;'
	FGBI = '38;5;'
	BGBI = '48;5;'

class StyleText(NoValue):
	Normal = 0
	Bold = 1 # Lighter normal
	Dark = 2 # Darker normal
	Italic = 3
	Underline = 4
	BlinkSlow = 5 # No work in Live CD/DVD/USB
	BlinkFast = 6 # Not work all
	Inverting = 7 # inverting color
	Hide = 8
	Strike = 9 # cross-out

@dataclass
class RGB:
	R: int # Red
	G: int # Green
	B: int # Blue

	@property
	def GetRGB(self):
		return (self.R, self.G, self.B)

@dataclass
class BiColor:
	BG: int # Background
	FG: int # Foreground

	@property
	def GetBi(self):
		return (self.BG, self.FG)

@dataclass
class Point:
	x: int
	y: int

	@property
	def GetPoint(self):
		return (self.x, self.y)

@dataclass
class Rect:
	point: Point
	width: int
	height: int

	@property
	def GetRect(self):
		return (self.point.x, self.point.y, self.width, self.height)

def hex_to_rgb(value: str):
	"""Return (red, green, blue) for the color given as #RRGGBB."""
	hexstr = value.lstrip('#')
	lv = len(hexstr)
	if lv == 1:
		v = int(hexstr, 16)*17
		return (v, v, v)
	if lv == 3:
		return tuple(int(hexstr[i:i+1], 16)*17 for i in range(0, 3))
	return tuple(int(hexstr[i:i+2], 16) for i in range(0, 6, 2))

def rgb2hex(r, g, b):
	return f'#{r:02x}{g:02x}{b:02x}'

def main():
	pass

if __name__ == '__main__':
	main()
