#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket

def main():
	s = socket.socket()
	address = 'localhost'
	port = 10000
	connected = False
	try:
		s.connect((address, port))
		connected = True
	except Exception as e:
		#print("something's wrong with %s:%d. Exception is %s" % (address, port, e))
		connected = False
	finally:
		s.close()
	print(connected)

if __name__ == '__main__':
	main()
