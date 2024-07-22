#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing.managers import BaseManager

class QueueManager(BaseManager):
	pass

def main():
	QueueManager.register('GetQueue')
	m = QueueManager(address=('localhost', 10000), authkey=b'abracadabra')
	m.connect()
	queue = m.GetQueue()
	#if queue.empty():
	queue.put('hello')
	
if __name__ == '__main__':
	main()
