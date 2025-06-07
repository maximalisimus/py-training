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

def convert_float_to_base(num, base, precision=5):
	""" Перевод дробных чисел из десятичной системы в заданную. """
	integer_part = int(num)
	fractional_part = num - integer_part

	integer_result = convert_to_base(integer_part, base)

	fractional_result = []
	while precision:
		fractional_part *= base
		digit = int(fractional_part)
		fractional_result.append(str(digit))
		fractional_part -= digit
		precision -= 1

	return f"{integer_result}.{''.join(fractional_result)}"

def convert_to_decimal(num_str, base):
	"""Перевод строки числа из заданной системы счисления в десятичную."""
	return int(num_str, base)

def convert_float_to_decimal(num_str, base):
	"""Перевод строки числа с плавающей точкой из заданной системы счисления в десятичную."""
	if '.' in num_str:
		integer_part, fractional_part = num_str.split('.')
	else:
		integer_part, fractional_part = num_str, '0'

	# Перевод целой части
	integer_decimal = int(integer_part, base)

	# Перевод дробной части
	fractional_decimal = 0
	for i, digit in enumerate(fractional_part):
		fractional_decimal += int(digit, base) / (base ** (i + 1))

	return integer_decimal + fractional_decimal

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

def convert_fraction_to_hex(fraction, precision=5):
	"""Перевод дробной части числа в шестнадцатеричную систему."""
	hex_fraction = []
	while precision:
		fraction *= 16
		digit = int(fraction)
		if digit < 10:
			hex_fraction.append(str(digit))
		else:
			hex_fraction.append(chr(digit - 10 + ord('A')))
		fraction -= digit
		precision -= 1

	return ''.join(hex_fraction)

def convert_float_to_hex(num):
	"""Перевод числа с плавающей точкой из десятичной системы в шестнадцатеричную."""
	if '.' in str(num):
		integer_part, fractional_part = str(num).split('.')
		integer_part = int(integer_part)
		fractional_part = float('0.' + fractional_part)
	else:
		integer_part = int(num)
		fractional_part = 0.0

	hex_integer = convert_integer_to_hex(integer_part)
	hex_fraction = convert_fraction_to_hex(fractional_part)

	return f"{hex_integer}.{hex_fraction}"

def hex_to_decimal(hex_str):
	"""Перевод строки числа с плавающей точкой из шестнадцатеричной системы в десятичную."""
	if '.' in hex_str:
		integer_part, fractional_part = hex_str.split('.')
	else:
		integer_part, fractional_part = hex_str, '0'

	# Перевод целой части
	integer_decimal = int(integer_part, 16)

	# Перевод дробной части
	fractional_decimal = 0
	for i, digit in enumerate(fractional_part):
		fractional_decimal += int(digit, 16) / (16 ** (i + 1))

	return integer_decimal + fractional_decimal

def is_integer(num_str):
	"""Определяет, является ли число целым или дробным."""
	if '.' in str(num_str):
		return False
	else:
		return True

def add_int_base(num1_str, num2_str, base):
	"""Сложение двух целых чисел в заданной системе счисления."""
	num1_decimal = convert_to_decimal(num1_str, base)
	num2_decimal = convert_to_decimal(num2_str, base)
	result_decimal = num1_decimal + num2_decimal
	return convert_to_base(result_decimal, base)

def subtract_int_base(num1_str, num2_str, base):
	"""Вычитание двух целых чисел в заданной системе счисления."""
	num1_decimal = convert_to_decimal(num1_str, base)
	num2_decimal = convert_to_decimal(num2_str, base)
	result_decimal = num1_decimal - num2_decimal
	return convert_to_base(result_decimal, base)

def division_int_base(num1_str, num2_str, base):
	"""Деление двух целых чисел в заданной системе счисления."""
	num1_decimal = convert_to_decimal(num1_str, base)
	num2_decimal = convert_to_decimal(num2_str, base)
	result_decimal = num1_decimal / num2_decimal
	return convert_to_base(result_decimal, base)

def multiplication_int_base(num1_str, num2_str, base):
	"""Деление двух целых чисел в заданной системе счисления."""
	num1_decimal = convert_to_decimal(num1_str, base)
	num2_decimal = convert_to_decimal(num2_str, base)
	result_decimal = num1_decimal * num2_decimal
	return convert_to_base(result_decimal, base)

def add_float_base(num1_str, num2_str, base):
	"""Сложение двух дробных чисел в заданной системе счисления."""
	num1_decimal = convert_float_to_decimal(num1_str, base)
	num2_decimal = convert_float_to_decimal(num2_str, base)
	result_decimal = num1_decimal + num2_decimal
	return convert_float_to_base(result_decimal, base)

def subtract_float_base(num1_str, num2_str, base):
	"""Вычитание двух дробных чисел в заданной системе счисления."""
	num1_decimal = convert_float_to_decimal(num1_str, base)
	num2_decimal = convert_float_to_decimal(num2_str, base)
	result_decimal = num1_decimal - num2_decimal
	return convert_float_to_base(result_decimal, base)

def division_float_base(num1_str, num2_str, base):
	"""Деление двух дробных чисел в заданной системе счисления."""
	num1_decimal = convert_float_to_decimal(num1_str, base)
	num2_decimal = convert_float_to_decimal(num2_str, base)
	result_decimal = num1_decimal / num2_decimal
	return convert_float_to_base(result_decimal, base)

def multiplication_float_base(num1_str, num2_str, base):
	"""Деление двух дробных чисел в заданной системе счисления."""
	num1_decimal = convert_float_to_decimal(num1_str, base)
	num2_decimal = convert_float_to_decimal(num2_str, base)
	result_decimal = num1_decimal * num2_decimal
	return convert_float_to_base(result_decimal, base)

def main():
	print()
	print(f"Выполнение различных операций с числами в заданной системе счисления.")
	user_one_number = input("Введите ваше первое число: ")
	user_two_number = input("Введите ваше второе число: ")
	user_base = input("Введите систему счисления веденных чисел: ")
	user_operation = input("Введите введите операцию над числами (+, -, /, *): ")
	
	isinteger_one = is_integer(user_one_number)
	isinteger_two = is_integer(user_two_number)
	
	if isinteger_one and isinteger_two:
		if user_operation == '+':
			print(f"{user_one_number} в {user_base} с.с. + {user_two_number} в {user_base} с.с. = {add_int_base(user_one_number, user_two_number, int(user_base))} в {user_base} с.с.")
		elif user_operation == '-':
			print(f"{user_one_number} в {user_base} с.с. - {user_two_number} в {user_base} с.с. = {subtract_int_base(user_one_number, user_two_number, int(user_base))} в {user_base} с.с.")
		elif user_operation == '/':
			print(f"{user_one_number} в {user_base} с.с. / {user_two_number} в {user_base} с.с. = {division_float_base(user_one_number, user_two_number, int(user_base))} в {user_base} с.с.")
		elif user_operation == '*':
			print(f"{user_one_number} в {user_base} с.с. * {user_two_number} в {user_base} с.с. = {multiplication_int_base(user_one_number, user_two_number, int(user_base))} в {user_base} с.с.")
	else:
		if user_operation == '+':
			print(f"{user_one_number} в {user_base} с.с. + {user_two_number} в {user_base} с.с. = {add_float_base(user_one_number, user_two_number, int(user_base))} в {user_base} с.с.")
		elif user_operation == '-':
			print(f"{user_one_number} в {user_base} с.с. - {user_two_number} в {user_base} с.с. = {subtract_float_base(user_one_number, user_two_number, int(user_base))} в {user_base} с.с.")
		elif user_operation == '/':
			print(f"{user_one_number} в {user_base} с.с. / {user_two_number} в {user_base} с.с. = {division_float_base(user_one_number, user_two_number, int(user_base))} в {user_base} с.с.")
		elif user_operation == '*':
			print(f"{user_one_number} в {user_base} с.с. * {user_two_number} в {user_base} с.с. = {multiplication_float_base(user_one_number, user_two_number, int(user_base))} в {user_base} с.с.")

if __name__ == '__main__':
	main()
