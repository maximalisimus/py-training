#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import system
from shutil import get_terminal_size

width, height = get_terminal_size()

def PrintPos(OnText: str = '', x: int = 0, y: int = 0):
	global width
	global height
	if (x < width and y < height and (len(OnText)+x) < width):
		if (x >= 0 and y >= 0):
			#print('{0:c}[{1:d};{2:d}f{3}'.format(0x1B, y, 0, ' '*width))
			print('{0:c}[{1:d};{2:d}f{3}'.format(0x1B, y, x, OnText))
		else:
			raise ValueError("Incorrect output position. Enter positive 'x' and 'y'.")
	else:
		if ((len(OnText)+x) >  width):
			raise ValueError("Incorrect output position. Enter a smaller value of 'x'.")
		elif (y > height):
			raise ValueError("Incorrect output position. Enter a smaller value of 'y'.")
		else:
			print(OnText)

def get_Midle_Text_Pos(theText: str) -> int:
	global width
	pos = int(width/2) - int(len(theText)/2)
	if ((pos+len(theText)) < width):
		return pos
	else:
		raise ValueError("The string is too long. Enter a shorter string.")

def PrintCenter(theText: str, y: int = 0):
	x = get_Midle_Text_Pos(theText)
	PrintPos(theText, x, y)

def main():
	global width
	global height
	system('clear')
	print(width, height)
	PrintPos('My text is available', 10, 10)
	PrintPos('My text is available', 10, 23)
	PrintCenter('My text is available', 0)
	PrintPos('', width-1, height-1)

if __name__ == '__main__':
	main()
