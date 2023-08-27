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

def main():
	paths = tuple(sorted(pathlib.Path('./test-dir/').rglob('.')))
	index_file = 'index.txt'
	for x in paths:
		with open(x.joinpath(index_file),'w') as f:
			f.write(f"Back ...\t-\t-\t-\n")
			dirs = map(lambda y: str(y.name), filter(lambda y: y.is_dir(), x.iterdir()))
			for y in sorted(dirs, key=str.lower, reverse=False):
				f.write(f"{y}\t-\t-\t-\n")
			files = map(lambda y: str(y.name), filter(lambda y: y.is_file(), x.iterdir()))
			for y in sorted(files, key=str.lower, reverse=False):
				if y != index_file: 
					fm = filemode(pathlib.Path(x).joinpath(y).stat().st_mode)
					sts = stampToStr(pathlib.Path(x).joinpath(y).stat().st_mtime, "%d-%b-%Y %H:%M")
					sf = size_format(pathlib.Path(x).joinpath(y).stat().st_size)
					f.write(f"{y}\t{fm}\t{sts}\t{sf}\n")
	pass

if __name__ == '__main__':
	main()
