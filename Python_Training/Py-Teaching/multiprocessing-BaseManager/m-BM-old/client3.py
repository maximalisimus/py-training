#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing.managers import BaseManager

class QueueManager(BaseManager):
	pass

def main():
	QueueManager.register('GetQueue')
	QueueManager.register('stop')
	m = QueueManager(address=('localhost', 10000), authkey=b'abracadabra')
	m.connect()
	m.stop()
	
if __name__ == '__main__':
	main()
