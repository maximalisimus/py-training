#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import signal
import sys

def main():
	on_pid = int(sys.argv[1])
	os.kill(on_pid, signal.SIGTERM)
	
if __name__ == '__main__':
	main()
