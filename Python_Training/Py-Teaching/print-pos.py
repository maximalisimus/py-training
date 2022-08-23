#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
from shutil import get_terminal_size

width, height = get_terminal_size()

def PrintPos(OnText: str, x: int = 0, y: int = 0):
	global width
	global height
	if (x < width and y < height):
		print('{0:c}[{1:d};{2:d}f{3}'.format(0x1B, y, 0, ' '*width))
		print('{0:c}[{1:d};{2:d}f{3}'.format(0x1B, y, x, OnText))
	else:
		print(OnText)

def main():
	print(width, height)
	PrintPos('My text is available', 10, 10)
	sleep(3)
	PrintPos('This is new text', 10, 10)	

if __name__ == '__main__':
	main()
