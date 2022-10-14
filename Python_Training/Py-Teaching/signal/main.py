#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import signal
import time
import os

def exit_handler(signum, frame):
	print('Exiting....')
	exit(0)

def main():
	#valid_signals = signal.valid_signals()
	#print(valid_signals)
	signal.signal(signal.SIGTERM, exit_handler)
	print(os.getpid())
	time.sleep(15)
	
if __name__ == '__main__':
	main()
