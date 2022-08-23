#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def hex2rgb(hex):
	return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def rgb2hex(r, g, b):
	return f'#{r:02x}{g:02x}{b:02x}'

def main():
	str_color = '#e61ed9'
	hex_color = str_color.lstrip('#')
	rgb_tuple = hex2rgb(hex_color)
	del hex_color
	print(rgb_tuple)
	new_str_color = rgb2hex(rgb_tuple[0], rgb_tuple[1], rgb_tuple[2])
	print(str_color, new_str_color)

if __name__ == '__main__':
	main()
