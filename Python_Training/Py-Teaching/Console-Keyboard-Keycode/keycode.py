#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from select import select

def ReadKey() -> str:
	rlist, wlist, xlist = select([sys.stdin], [], [])
	if rlist:
		key = sys.stdin.read(1)
		if key == '\x1b':
			# Если escape последовательность, то считать еще 2 символа 
			# Но будет некорректно работать, если был нажата клавиша Escape (будет ждать нажатия еще 2 кнопок)
			key += sys.stdin.read(2)
		if key == '\x1b[A':
			return 'Up'
		elif key == '\x1b[B':
			return 'Down'
		elif key == '\x1b[C':
			return 'Right'
		elif key == '\x1b[D':
			return 'Left'

def main():
    keycode = ReadKey()
    print(keycode)

if __name__ == '__main__':
	main()
