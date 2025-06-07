#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def convert_to_base(num, base):
	""" Перевод целых чисел из десятичной системы в заданную. """
	if num < 0:
		return '-' + convert_to_base(-num, base)
	elif num == 0:
		return '0'

	digits = []
	while num:
		digits.append(int(num % base))
		num //= base

	return ''.join(str(x) for x in digits[::-1])

def convert_to_decimal(num_str, base):
	"""Перевод строки числа из заданной системы счисления в десятичную."""
	return int(num_str, base)

def convert_integer_to_hex(num):
	"""Перевод целой части числа в шестнадцатеричную систему."""
	if num < 0:
		return '-' + convert_integer_to_hex(-num)
	elif num == 0:
		return '0'
	
	hex_digits = []
	while num:
		remainder = num % 16
		if remainder < 10:
			hex_digits.append(str(remainder))
		else:
			hex_digits.append(chr(remainder - 10 + ord('A')))  # Преобразование в символы A-F
		num //= 16
	
	return ''.join(hex_digits[::-1])

def main():
	print()
	print(f"Перевод целых чисел из заданной системы счисления в указанную пользователем.")
	user_number = input("Введите ваше целое число для конвертации: ")
	user_input_base = input("Введите систему счисления из которой конвертируем: ")
	user_output_base = input("Введите систему счисления в которую надо конвертировать: ")
	if user_output_base == 16:
		print(f"Число {user_number} в {user_input_base} с.с. = {convert_integer_to_hex(convert_to_decimal(str(user_number), int(user_input_base)))} в 16 с.с.")
	else:
		print(f"Число {user_number} в {user_input_base} с.с. = {convert_to_base(convert_to_decimal(str(user_number), int(user_input_base)), int(user_output_base))} в {user_output_base} с.с.")
	print()

if __name__ == '__main__':
	main()
