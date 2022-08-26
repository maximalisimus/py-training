#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from win32com.client import GetObject

from datetime import datetime

def dateTimeToStr(dateTime: datetime, strFormat = "%d.%m.%Y-%H:%M:%S") -> str:
	outDateTime = dateTime.strftime(strFormat)
	return outDateTime

def strToDateTime(dateStr: str, strFormat = "%d.%m.%Y-%H:%M:%S") -> datetime:
	time_Tuple = datetime.strptime(dateStr, strFormat)
	return time_Tuple

def OnWinmgmts(OnObject: str):
	root_winmgmts = GetObject("winmgmts:root\cimv2")
	on_root = root_winmgmts.ExecQuery("Select * from " + OnObject)
	return on_root

def GetFullPrograms():
	programs = OnWinmgmts('Win32_Product')
	a = set()
	for x in programs:
		on_date_str = dateTimeToStr(strToDateTime(x.InstallDate, "%Y%m%d"), "%d.%m.%Y")
		#yield f"{x.Name}, {x.Version}, {on_date_str}, {x.InstallLocation}"
		yield (f"{x.Name}", f"{x.Version}", f"{on_date_str}", f"{x.InstallLocation}")

def main():
	full_programs = sorted(GetFullPrograms(), key=lambda x: x[0])
	with open('programs.txt', 'w') as f:
		f.write(f"Windows programs:\n")
		for i in full_programs:
			f.write(f"\t{', '.join(i)}\n")

if __name__ == '__main__':
	main()
