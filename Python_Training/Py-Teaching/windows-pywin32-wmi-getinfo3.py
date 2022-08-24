#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from win32com.client import GetObject

def size_format(in_size):
	if in_size < 1000:
		return f"{in_size} B"
	elif 1000 <= in_size < 1000000:
		#return '%.1f' % float(in_size/1000) + ' KB'
		return f"{float(in_size/1000):.1f} KB"
	elif 1000000 <= in_size < 1000000000:
		#return '%.1f' % float(in_size/1000000) + ' MB'
		return f"{float(in_size/1000000):.1f} MB"
	elif 1000000000 <= in_size < 1000000000000:
		# return '%.1f' % float(in_size/1000000000) + ' GB'
		return f"{float(in_size/1000000000):.1f} GB"
	elif 1000000000000 <= in_size:
		#return '%.1f' % float(in_size/1000000000000) + ' TB'
		return f"{float(in_size/1000000000000):.1f} TB"

def OnWinmgmts(OnObject: str):
	root_winmgmts = GetObject("winmgmts:root\cimv2")
	on_root = root_winmgmts.ExecQuery("Select * from " + OnObject)
	return on_root

def GetCPUType():
	cpus = OnWinmgmts('Win32_Processor')
	for x in cpus:
		output = f"{str(x.Name).strip()}, L2CacheSize = {str(size_format(x.L2CacheSize)).strip()}, " + \
				f"L3CacheSize = {str(size_format(x.L3CacheSize)).strip()}, " + \
				f"Cores = {str(x.NumberOfCores).strip()}, Thread = {str(x.NumberOfLogicalProcessors).strip()}"
		yield output

def GetMemory():
	memory = OnWinmgmts('Win32_PhysicalMemory')
	for x in memory:
		yield f"{x.Name}: {str(x.PartNumber).strip()}, {str(x.Speed).strip()} MHz, {size_format(int(x.Capacity))}"

def GetVideoControllerInfo():
	videocontroller = OnWinmgmts('Win32_VideoController')
	for x in videocontroller:
		yield f"{str(x.Name).strip()}, {str(x.VideoModeDescription).strip()}"

def GetPrinters():
	printers = OnWinmgmts('Win32_Printer')
	for x in printers:
		yield f"{x.Name}".replace('\n', '').strip()

def main():
	cpu_info = GetCPUType()
	print('CPU Info:')
	for i in cpu_info:
		print(f"\t{i}")
	video_info = GetVideoControllerInfo()
	print('VideoCards:')
	for i in video_info:
		print(f"\t{i}")
	lst_printers = GetPrinters()
	print('Printers:')
	for i in lst_printers:
		print(f"\t{i}")
	on_memory = GetMemory()
	for i in on_memory:
		print(f"{i}")

if __name__ == '__main__':
	main()
