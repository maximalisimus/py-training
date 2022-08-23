#!/usr/bin/env python3
# -*- coding: utf-8 -*-


ltop = '┌'
rtop = '┐'
vert = '│'
middle = '─'
lbottom = '└'
rbottom = '┘'

def Border_Text(onText: str) -> str:
	tmp_text = ''
	count_text = len(onText)
	top_text = ltop + middle*(count_text+2) + rtop
	middle_text = vert + ' ' + onText + ' ' + vert
	bottom_text = lbottom + middle*(count_text+2) + rbottom
	return (top_text, middle_text, bottom_text)

def main():
	btn1 = Border_Text('OK')
	btn2 = Border_Text('Cancel')
	btn3 = Border_Text('Abort')
	buttons = f"{btn3[0]} {btn1[0]} {btn2[0]}\n{btn3[1]} {btn1[1]} {btn2[1]}\n{btn3[2]} {btn1[2]} {btn2[2]}"
	print(buttons)

if __name__ == '__main__':
	main()
