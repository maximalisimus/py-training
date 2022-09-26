#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pathlib
from os import mkfifo

def main():
	# pathlib.Path.home()
	FIFO = pathlib.Path(sys.argv[0]).parent.joinpath('pipe1').resolve()
	if not FIFO.exists():
		mkfifo(FIFO)
	print("Opening FIFO...")
	with open(FIFO) as fifo:
		print("FIFO opened")
		while True:
			data = fifo.read()
			if len(data) == 0:
				print("Writer closed")
				break
			print(f"{data}")
	FIFO.unlink(missing_ok=True)

if __name__ == '__main__':
	main()
