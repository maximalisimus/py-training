#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Normal RGB to BG and RGB to Text: text-color, bg-color
# printf "\x1b[38;2;40;200;249;249m\x1b[48;2;250;122;241mTRUECOLOR\x1b[0m\n"
#
# Mode set text attribute: bg-color, text-color
# printf "\x1b[38;2;40;200;249;249m\x1b[5;48;2;250;122;241mTRUECOLOR\x1b[0m\n"
#
# Normal Mode, One Color BG and One Color Text Color
# printf "\x1b[38;5;45m\x1b[48;5;207mTRUECOLOR\x1b[0m\n"
# 0 - normal
# 1 - bold (lighter normal)
# 2 - darker normal
# 3 - italic
# 4 - underline
# 5 - blink (slow)
# 6 - blink (fast)
# 7 - inverting color
# 8 - hide
# 9 - cross-out
#
# Mode set text attribute
# printf "\x1b[38;5;45m\x1b[0;48;5;207mTRUECOLOR\x1b[0m\n"
# printf "\x1b[38;5;45m\x1b[1;48;5;207mTRUECOLOR\x1b[0m\n"
# printf "\x1b[38;5;45m\x1b[4;48;5;207mTRUECOLOR\x1b[0m\n"
# printf "\x1b[38;5;45m\x1b[5;48;5;207mTRUECOLOR\x1b[0m\n"
# printf "\x1b[38;5;45m\x1b[7;48;5;207mTRUECOLOR\x1b[0m\n"
# printf "\x1b[38;5;45m\x1b[8;48;5;207mTRUECOLOR\x1b[0m\n"
# 0 - normal
# 1 - bold (lighter normal)
# 2 - darker normal
# 3 - italic
# 4 - underline
# 5 - blink (slow)
# 6 - blink (fast)
# 7 - inverting color
# 8 - hide
# 9 - cross-out

def main():
	# Bold
	print('\x1b[38;2;40;200;249;249m\x1b[48;2;250;122;241mTRUECOLOR\x1b[0m\n')
	# Normal
	print('\x1b[38;5;45m\x1b[48;5;207mTRUECOLOR\x1b[0m\n')
	

if __name__ == '__main__':
	main()
