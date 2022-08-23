#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ctypes
from ctypes.wintypes import BYTE, DWORD, LPCWSTR

def GetPrinters():
	winspool = ctypes.WinDLL('winspool.drv')  # for EnumPrintersW
	msvcrt = ctypes.cdll.msvcrt  # for malloc, free

	# Parameters: modify as you need. See MSDN for detail.
	PRINTER_ENUM_LOCAL = 2
	Name = None  # ignored for PRINTER_ENUM_LOCAL
	Level = 1  # or 2, 4, 5

	class PRINTER_INFO_1(ctypes.Structure):
		_fields_ = [
			("Flags", DWORD),
			("pDescription", LPCWSTR),
			("pName", LPCWSTR),
			("pComment", LPCWSTR),
		]

	# Invoke once with a NULL pointer to get buffer size.
	info = ctypes.POINTER(BYTE)()
	pcbNeeded = DWORD(0)
	pcReturned = DWORD(0)  # the number of PRINTER_INFO_1 structures retrieved
	winspool.EnumPrintersW(PRINTER_ENUM_LOCAL, Name, Level, ctypes.byref(info), 0,
			ctypes.byref(pcbNeeded), ctypes.byref(pcReturned))

	bufsize = pcbNeeded.value
	buffer = msvcrt.malloc(bufsize)
	winspool.EnumPrintersW(PRINTER_ENUM_LOCAL, Name, Level, buffer, bufsize,
			ctypes.byref(pcbNeeded), ctypes.byref(pcReturned))
	info = ctypes.cast(buffer, ctypes.POINTER(PRINTER_INFO_1))
	#for i in range(pcReturned.value):
	#	print(info[i].pName)#, '=>', info[i].pDescription
	msvcrt.free(buffer)
	for i in range(pcReturned.value):
		yield f"{info[i].pName}"

def main():
	lst_printer = GetPrinters()
	print(tuple(lst_printer))
	pass

if __name__ == '__main__':
	main()
