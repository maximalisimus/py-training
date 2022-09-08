#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib

def main():
	paths = tuple(sorted(pathlib.Path('./').rglob('.')))
	index_file = 'index.txt'
	for x in paths:
		with open(x.joinpath(index_file),'w') as f:
			dirs = map(lambda y: str(y.name), filter(lambda y: y.is_dir(), x.iterdir()))
			for y in sorted(dirs, key=str.lower, reverse=False):
				f.write(f"{y}\n")
			files = map(lambda y: str(y.name), filter(lambda y: y.is_file(), x.iterdir()))
			for y in sorted(files, key=str.lower, reverse=False):
				if y != index_file: f.write(f"{y}\n")
	pass

if __name__ == '__main__':
	main()
