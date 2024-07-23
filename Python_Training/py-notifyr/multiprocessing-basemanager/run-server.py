#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib
import subprocess
import sys
import platform

def RunServer():
	python = str(pathlib.Path(str(sys.executable)).resolve())
	script = str(pathlib.Path('./server2.py').resolve())
	cmd = []
	if  platform.system() == 'Windows':
		cmd = ['start', '/b', python, script]
	else:
		cmd = [python, script, '&']
	result = subprocess.run(cmd, shell=True)

def main():
	RunServer()

if __name__ == '__main__':
	main()
