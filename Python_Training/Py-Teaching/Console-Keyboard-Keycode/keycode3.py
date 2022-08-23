#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pip install getkey

from getkey import getkey, key

def main():
	#print("press enter")
	var = getkey()

	if var == key.ENTER:
		print("You pressed enter")
	elif  var == key.UP:
		print("You pressed UP")
	elif  var == key.DOWN:
		print("You pressed DOWN")
	elif  var == key.RIGHT:
		print("You pressed RIGHT")
	elif  var == key.LEFT:
		print("You pressed LEFT")
	elif  var == key.ESC:
		print("You pressed ESC")
	elif  var == key.SPACE:
		print("You pressed SPACE")
	else:
		print("You didnt")

if __name__ == '__main__':
	main()
