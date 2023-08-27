#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib
from stat import filemode
from datetime import datetime

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

def stampToStr(timeStamp: int, strFormat = "%d.%m.%Y-%H:%M:%S") -> str:
	dateTime = datetime.fromtimestamp(timeStamp)
	datestr = dateTime.strftime(strFormat)
	return datestr

p = pathlib.Path( 'main.py' )

print(filemode(p.stat().st_mode))
print(size_format(p.stat().st_size))
strFormat = "%d.%m.%Y-%H:%M:%S"
print(stampToStr(p.stat().st_mtime, "%d-%b-%Y %H:%M"))

