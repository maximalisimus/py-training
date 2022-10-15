#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib
import os
import threading

def RunServer():
	os.system(pathlib.Path('./server.py').resolve())

def main():
	th = threading.Thread(target=RunServer, args=(), daemon=True)
	th.start()

if __name__ == '__main__':
	main()
