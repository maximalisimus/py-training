#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def main():
	print('Mode:', end = ' ')
	print('\x1b[0;38;5;255m\x1b[48;5;0mNormal\x1b[0m', end = ' ')
	print('\x1b[1;38;5;255m\x1b[48;5;0mBold\x1b[0m', end = ' ')
	print('\x1b[4;38;5;255m\x1b[48;5;0mUnderline\x1b[0m', end = ' ')
	print('\x1b[5;38;5;255m\x1b[48;5;0mBlink\x1b[0m', end = ' ')
	print('\x1b[7;38;5;255m\x1b[48;5;0mInvert\x1b[0m', end = ' ')
	print('\x1b[8;38;5;255m\x1b[48;5;0mHide\x1b[0m', end = ' ')
	print()
	print('Normal text color:')
	for item in range(0,256):
		print(f"\x1b[0;38;5;{item}m\x1b[48;5;0m{item}\x1b[0m", end = ' ')
	print()
	print('Bold text color:')
	for item in range(0,256):
		print(f"\x1b[1;38;5;{item}m\x1b[48;5;0m{item}\x1b[0m", end = ' ')
	print()
	print('Background normal text color:')
	for item in range(0,256):
		print(f"\x1b[0;48;5;{item}m\x1b[38;5;255m{item}\x1b[0m", end = ' ')
	print()
	print('Background bold text color:')
	for item in range(0,256):
		print(f"\x1b[1;48;5;{item}m\x1b[38;5;255m{item}\x1b[0m", end = ' ')
	print()

if __name__ == '__main__':
	main()
