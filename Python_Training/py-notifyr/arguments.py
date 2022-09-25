#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum
import pathlib

class NoValue(Enum):

	def __repr__(self):
		return f"{self.__class__}: {self.name}"
	
	def __str__(self):
		return f"{self.name}"
	
	def __call__(self):
		return f"{self.value}"

class Weight(NoValue):
	normal = 'normal'
	bold = 'bold'
	
	@classmethod
	def GetWeight(cls, weight: str):
		for x in cls:
			if weight == x.value:
				return x
		return None

class PositionX(NoValue):
	Left = 'left'
	Right = 'right'
	Center = 'center'
	
	@classmethod
	def GetPos(cls, pos: str):
		for x in cls:
			if pos == x.value:
				return x
		return None

class PositionY(NoValue):
	Top = 'top'
	Center = 'center'
	Bottom = 'Bottom'

	@classmethod
	def GetPos(cls, pos: str):
		for x in cls:
			if pos == x.value:
				return x
		return None

class Arguments:
	
	__slots__ = 'title text on_time icon fonts fg_color bg_color scale width height pos_x pos_y alpha top left'.split()
	
	def __init__(self, *args, **kwargs):
		self.title = args[0] if len(args) >= 1 else kwargs.get('title', 'Apps')
		self.text = args[1] if len(args) >= 2 else kwargs.get('text', 'Ok!')
		self.on_time = args[2] if len(args) >= 3 else kwargs.get('on_time', 10000)
		self.icon = pathlib.Path(args[3]).resolve() if len(args) >= 4 else kwargs.get('icon', '')
		self.fonts = list(str(args[4]).split(',')) if len(args) >= 5 else list(str(kwargs.get('fonts','Arial,14,normal')).split(','))
		self.fonts[1] = int(self.fonts[1])
		self.fonts[2] = Weight.GetWeight(self.fonts[2])
		self.fonts = tuple(self.fonts)
		self.fg_color = args[5] if len(args) >= 6 else kwargs.get('fg_color', 'black')
		self.bg_color = args[6] if len(args) >= 7 else kwargs.get('bg_color', '#FFFADD')
		self.scale = tuple(map(int, str(args[7]).split(',')))  if len(args) >= 8 else tuple(map(int, str(kwargs.get('scale', '1,1')).split(',')))
		self.width = args[8] if len(args) >= 9 else kwargs.get('width', 200)
		self.height = args[9] if len(args) >= 10 else kwargs.get('height', 100)
		self.pos_x = PositionX.GetPos(args[10]) if len(args) >= 11 else PositionX.GetPos(kwargs.get('pos_x', 'right'))
		self.pos_y = PositionY.GetPos(args[11]) if len(args) >= 12 else PositionY.GetPos(kwargs.get('pos_y', 'top'))
		self.alpha = args[12] if len(args) >= 13 else kwargs.get('alpha', 1.0)
		self.top = args[13] if len(args) >= 14 else kwargs.get('top', 0)
		self.left = args[14] if len(args) >= 15 else kwargs.get('left', 0)

	def __repr__(self):
		return f"{self.__class__}:" + \
				f"\n\tTitle: {self.title}" + \
				f"\n\tText: {self.text}" + \
				f",\n\tTime: {self.on_time} ms" + \
				f",\n\tIcon: {self.icon if self.icon != '' else None}," + \
				f"\n\tFonts: {self.fonts}," + \
				f"\n\tFG Color: {self.fg_color}, " + \
				f"BG Color: {self.bg_color}, " + \
				f"\n\tScale: {self.scale}, width: {self.width}, height: {self.height}," + \
				f"\n\tPos X: {self.pos_x}, Pos Y: {self.pos_y}," + \
				f"\n\tAlpha: {self.alpha}," + \
				f"\n\tTop: {self.top}, Left: {self.left}"

def main():
	arg = Arguments()
	print(arg)
	pass

if __name__ == '__main__':
	main()
