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
	print(queue.qsize())
	if not queue.empty():
		print(queue.get())
		queue.task_done()
	else:
		print('Queue is empty!')
	print(queue.qsize())
	
if __name__ == '__main__':
	main()
