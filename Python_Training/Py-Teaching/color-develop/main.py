#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum
from dataclasses import dataclass

from os import system
from shutil import get_terminal_size
import re

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

class HexColor(NoValue):
	Black = '#000000'
	Red = '#FF0000'
	Green = '#008000'
	DarkGreen = '#006400'
	YellowGreen = '#9ACD32'
	Brown = '#aa5500'
	Brown2 = '#A52A2A'
	OrangeRed = '#FF4500'
	DarkOrange = '#FF8C00'
	Orange = '#FFA500'
	Blue = '#0000FF'
	Purple = '#800080'
	Cyan = '#00FFFF'
	Yellow = '#FFFF00'
	LightRed = '#FF7377'
	LightGreen = '#90EE90'
	LightBlue = '#ADD8E6'
	LightPurple = '#975898'
	LightCyan = '#E0FFFF'
	White = '#FFFFFF'
	Chocolate = '#D2691E'
	Pink = '#FFC0CB'
	LightPink = '#FFB6C1'
	HotPink = '#FF69B4'
	Gray = '#808080'
	LightGray = '#D3D3D3'
	DarkGray = '#A9A9A9'
	Silver = '#C0C0C0'
	Aqua = '#00FFFF'
	Fuchsia = '#FF00FF'
	Maroon = '#800000'
	Olive = '#808000'
	Lime = '#00FF00'
	Goldenrod = '#DAA520'
	DarkGoldenRod = '#B8860B'
	Gold = '#FFD700'
	Coral = '#FF7F50'
	Bisque = '#FFE4C4'
	Tomato = '#FF6347'

class BorderSymbols(NoValue):
	''' https://unicode-table.com/ru/ '''
	Left_Up_Radius = '╭'
	Left_Up_Corn = '┌'
	Right_Up_Radius = '╮'
	Right_Up_Corn = '┐'
	Left_Down_Radius = '╰'
	Left_Down_Corn = '└'
	Right_Down_Radius = '╯'
	Right_Down_Corn = '┘'
	Three_Vertial_Right = '├'
	Three_Vertical_Left = '┤'
	Three_Horizontal_Down = '┬'
	Three_Horizontal_Up = '┴'
	Four = '┼'
	Right_Slach = '╱'
	Left_Slash = '╲'
	X = '╳'
	Line_Horizontal = '─'
	Line_Vertical = '│'
	Line_Vertial_Up = '╵'
	Line_Vertical_Down = '╷'
	Line_Horizontal_Left = '╴'
	Line_Horizontal_Right = '╶'
	Circle = '⬤'
	Close = '⭙'
	Info = '🛈'

class EscSeq(NoValue):
	ESC = '\x1b['
	END_ESC = '\x1b[0m'
	END_COLOR = 'm'

class ColorType(NoValue):
	#FG = '38;2;40'
	FG = '38;2'
	BG = '48;2'

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
class Point:
	x: int
	y: int

def HexToRGB(value: str):
	""" Return (red, green, blue) color from HEX value #RRGGBB """
	hexstr = value.lstrip('#')
	lv = len(hexstr)
	if lv == 1:
		v = int(hexstr, 16)*17
		return (v, v, v)
	elif lv == 3:
		return tuple(int(hexstr[i:i+1], 16)*17 for i in range(0, 3))
	elif lv == 6:
		return tuple(int(hexstr[i:i+2], 16) for i in range(0, 6, 2))
	else:
		return (0, 0, 0)

def RGBToHEX(r, g, b):
	""" Return HEX value on #RRGGBB from (red, green, blue) color """
	return f'#{r:02x}{g:02x}{b:02x}'

class BaseColorProperty:
	''' Property to Base Color RGB class '''
	
	__slots__ = ()
	
	@property
	def GetStr(self) -> str:
		''' Get Color to string value '''
		red, green, blue = HexToRGB(self.Colors)
		if self.TypeColor == ColorType.FG:
			if self.Style == StyleText.Normal:
				return f"{EscSeq.ESC.value}{self.TypeColor.value};{red};{green};{blue}{EscSeq.END_COLOR.value}"
			else:
				return f"{EscSeq.ESC.value}{self.Style.value};{self.TypeColor.value};{red};{green};{blue}{EscSeq.END_COLOR.value}"
		else:
			if self.TwoStyle == StyleText.Normal:
				return f"{EscSeq.ESC.value}{self.TypeColor.value};{red};{green};{blue}{EscSeq.END_COLOR.value}"
			else:
				return f"{EscSeq.ESC.value}{self.TwoStyle.value};{self.TypeColor.value};{red};{green};{blue}{EscSeq.END_COLOR.value}"


class BaseColor(BaseColorProperty):
	''' Class Base Color on RGB
	
		class init params:
			Colors - foreground text color
			Style - style text - Normal, Bold, Dark, 
								Italic, Underline, 
								BlinkSlow, BlinkFast, 
								Inverting, Hide, Strike
			TypeColor - background or foreground color
	'''

	__slots__ = 'Colors Style TypeColor TwoStyle'.split()

	def __init__(self, OnColor: str = '#ffffff', 
				OnStyle: StyleText = StyleText.Normal, 
				OnTypeColor: ColorType = ColorType.FG, 
				OnTwoStyle: StyleText = StyleText.Normal):
		''' BaseColor init
			
			OnColor - Colors. Foreground text color
			OnStyle - Style. Style text:
					Normal, Bold, Dark, 
					Italic, Underline, 
					BlinkSlow, BlinkFast, 
					Inverting, Hide, Strike
			OnTypeColor - background or foreground color
			TwoStyle - Two Style text - Right.
		 '''
		self.Colors: str = OnColor if '#' in OnColor else '#ffffff'
		self.Style: StyleText = OnStyle
		self.TypeColor: ColorType = OnTypeColor
		self.TwoStyle: StyleText = OnTwoStyle

	def __repr__(self):
		''' Debug '''
		return f"{self.__class__}: \n\t({self.Colors}: {HexToRGB(self.Colors)},\n\t {self.Style}, {self.TypeColor}, {self.TwoStyle})"

class FullColor_Property:
	
	__slots__ = ()
	
	def SetInvertColor(self):
		tmpBGColor = self.FG.Colors
		tmpFGColor = self.BG.Colors
		self.BG.Colors = tmpBGColor
		self.FG.Colors = tmpFGColor
	
	@property
	def GetStr(self) -> str:
		if (not self.isFG and self.FG.Style == StyleText.Inverting): self.SetInvertColor()
		if (not self.isBG and self.BG.Style == StyleText.Inverting): self.SetInvertColor()
		rez1 = f"{self.FG.GetStr}" if self.isFG else f""
		rez2 = f"{self.BG.GetStr}" if self.isBG else f""
		rez = rez1 + rez2
		return rez

class FullColor(FullColor_Property):
	''' class on FullColor 
	
		BG - Background BaseColor (class)
		FG - Foreground BaseColor (class)
		isBG - Whether to use Background BaseColor (class)
		isFG - Whether to use Foreground BaseColor (class)
	'''
	
	__slots__ = 'BG FG isBG isFG'.split()
	
	def __init__(self, 
				BG: BaseColor = BaseColor('#000000', StyleText.Normal, ColorType.BG), 
				FG: BaseColor = BaseColor('#ffffff', StyleText.Normal, ColorType.FG),
				isBG: bool = True,
				isFG: bool = True):
		self.BG: BaseColor = BG
		self.FG: BaseColor = FG
		self.isBG: bool = isBG
		self.isFG: bool = isFG
	
	def __repr__(self):
		return f"{self.__class__}: \n\t({self.BG},\n\t {self.FG},\n\t isBG: {self.isBG}, isFG: {self.isFG})"

class PositionProperty:
	
	__slots__ = ()
	
	@property
	def GetStr(self) -> str:
		''' Get position output elements'''
		# print(f"{0x1B:c}[{x};{y}fTextValue")
		if (self.point.x < self.width and self.point.y < self.height): # and (len(self.OnText)+self.point.x) < self.width):
			if (self.point.x >= 0 and self.point.y >= 0):				
				return f"{0x1B:c}[{self.point.y};{self.point.x}f"
			else:
				raise ValueError("Incorrect output position. Enter positive 'point.x' and 'point.y'.")
		else:
			#if ((len(self.OnText)+self.point.x) >  self.width):
			#	raise ValueError("Incorrect output position. Enter a smaller value of 'point.x'.")
			#el
			if (self.point.y > self.height):
				raise ValueError("Incorrect output position. Enter a smaller value of 'point.y'.")
			else:
				return ''
	
	@property
	def GetMiddleStr(self) -> int:
		''' Get Position output object center '''
		onpos = int(self.width/2) - int(len(self.OnText)/2)
		if ((onpos+len(self.OnText)) < self.width):
			#return onpos
			return f"{0x1B:c}[{self.point.y};{onpos}f"
		else:
			raise ValueError("The string is too long. Enter a shorter string.")

	def CenterText(self, sep = '\n') -> str:
		''' Center the text by the separator 'sep' and the width of the terminal '''
		onsep = sep + '+'
		for item in re.split(onsep, self.OnText):
			yield item.center(self.width-1)

class Position(PositionProperty):
	
	''' class Position output text '''
	
	__slots__ = 'OnText point width height'.split() # isLongStr
	
	def __init__(self, point: Point = Point(0, 0), OnText: str = ''): #, isLongStr: bool = False):
		''' Init Position 
			
			x: Position on x symbols value
			y: Positon on y symbols value
			width: Fixed calculate terminal symbols size on x
			height: Fixed calculate terminal symbols size on y
		'''
		self.width, self.height = get_terminal_size()
		self.point: Point = point
		self.OnText: str = OnText
		#self.isLongStr: str = isLongStr

	def __repr__(self):
		return f"{self.__class__}: (width: {self.width}, height: {self.height}, {self.point})"

def BaseExample():
	'''
	# BaseColor Test
	fcolor = BaseColor('#c8f9f9', StyleText.Bold, ColorType.FG)
	bcolor = BaseColor('#fa7af1', StyleText.Normal, ColorType.BG)
	print(f"{fcolor.GetStr}{bcolor.GetStr}TRUECOLOR{EscSeq.END_ESC.value}")
	print("\x1b[1;38;2;40;200;249;249m\x1b[48;2;250;122;241mTRUECOLOR\x1b[0m")
	fcolor.Style = StyleText.Normal
	print(f"{fcolor.GetStr}{bcolor.GetStr}TRUECOLOR{EscSeq.END_ESC.value}")
	print("\x1b[0;38;2;40;200;249;249m\x1b[48;2;250;122;241mTRUECOLOR\x1b[0m")
	'''
	''' 
	# FullColor Test
	mycolor = FullColor()
	#mycolor.isBG = False
	mycolor.FG.Colors = '#0'
	mycolor.BG.Colors = '#f'
	print(mycolor)
	print(f"{mycolor.GetStr}TRUECOLOR{EscSeq.END_ESC.value}")
	# Debug view ALL Color string
	# with open('log.txt', 'a') as f:
	#	f.write(mycolor.GetStr)
	#	f.write('\n')
	mycolor.FG.Colors = '#c8f9f9'
	mycolor.FG.Style = StyleText.Bold
	mycolor.isBG = True
	# mycolor.FG.TypeColor = ColorType.FG
	# mycolor.FG.TwoStyle = StyleText.Bold
	mycolor.BG.Colors = '#fa7af1'
	mycolor.BG.Style = StyleText.Inverting
	#mycolor.BG.TwoStyle = StyleText.Inverting
	#mycolor.FG.Style = StyleText.Inverting
	mycolor.isBG = False
	print(mycolor)
	print(f"{mycolor.GetStr}TRUECOLOR{EscSeq.END_ESC.value}")
	# Debug view ALL Color string
	# with open('log.txt', 'a') as f:
	#	f.write(mycolor.GetStr)
	#	f.write('\n')
	mycolor.FG.Style = StyleText.Bold
	mycolor.BG.Style = StyleText.Normal
	mycolor.isBG = True
	mycolor.isFG = True
	mycolor.SetInvertColor()
	print(mycolor)
	print(f"{mycolor.GetStr}TRUECOLOR{EscSeq.END_ESC.value}")
	# with open('log.txt', 'a') as f:
	#	f.write(mycolor.GetStr)
	#	f.write('\n')
	'''
	'''
	# Position Test
	system('clear')
	pos = Position(Point(10, 10))
	pos.point.x = 20
	pos.point.y = 5
	print(pos)
	print(f"{pos.GetStr}TextValue")
	pos.point.x = 10
	pos.point.y = 7
	pos.OnText = '< Header H1 >'
	print(pos)
	print(f"{pos.GetMiddleStr}{pos.OnText}")
	'''
	'''
	# Position + BaseColor Test
	fcolor = BaseColor('#c8f9f9', StyleText.Bold, ColorType.FG)
	bcolor = BaseColor('#fa7af1', StyleText.Normal, ColorType.BG)
	system('clear')
	pos = Position(Point(5, 5))
	print(pos)
	print(f"{pos.GetStr}{fcolor.GetStr}{bcolor.GetStr}TRUECOLOR{EscSeq.END_ESC.value}")
	pos.point.y+=1
	print(f"{pos.GetStr}\x1b[1;38;2;40;200;249;249m\x1b[48;2;250;122;241mTRUECOLOR\x1b[0m")
	pos.point.y+=1
	fcolor.Style = StyleText.Normal
	print(f"{pos.GetStr}{fcolor.GetStr}{bcolor.GetStr}TRUECOLOR{EscSeq.END_ESC.value}")
	pos.point.y+=1
	print(f"{pos.GetStr}\x1b[0;38;2;40;200;249;249m\x1b[48;2;250;122;241mTRUECOLOR\x1b[0m")
	'''
	'''
	# Center terminal text
	system('clear')
	a = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit,\n sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
	pos = Position(Point(0, 5))
	pos.OnText = a
	for i in pos.CenterText():
		print(f"{pos.GetStr}{i}")
		pos.point.y+=1
	#print(f"{pos.GetStr}TextValue")
	'''
	'''
	# Print All HexColor
	mycolor = FullColor()
	mycolor.FG.Colors = HexColor.Black.value
	count = 0
	for item in HexColor:
		if count == 5:
			print()
			count = 0
		mycolor.BG.Colors = item.value
		print(f"{mycolor.GetStr} {item.name} {EscSeq.END_ESC.value}", end=' ')
		count+=1
	print()
	'''
	pass

def main():
	BaseExample()
	pass

if __name__ == '__main__':
	main()
