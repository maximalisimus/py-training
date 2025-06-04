#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def print_hello(language):
	match language:
		case "russian":
			print("Привет")
		case "english":
			print("Hello")
		case "german":
			print("Hallo")
		case _:
			print("Undefined")

def main():
	print_hello("english") # Hello
	print_hello("german") # Hallo
	print_hello("russian") # Привет
	print_hello("spanish") # Undefined
	pass

if __name__ == '__main__':
	main()
