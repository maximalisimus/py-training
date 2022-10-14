#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing.managers import BaseManager

class QueueManager(BaseManager):
	pass

def main():
	QueueManager.register('get_queue')
	m = QueueManager(address=('localhost', 10000), authkey=b'abracadabra')
	m.connect()
	queue = m.get_queue()
	print(queue.get())
	print(queue.get())
	
if __name__ == '__main__':
	main()
