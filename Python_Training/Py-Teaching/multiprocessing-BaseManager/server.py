#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing.managers import BaseManager
from queue import Queue

class QueueManager(BaseManager):
	pass

def main():
	queue = Queue()
	QueueManager.register('get_queue', callable=lambda:queue)
	m = QueueManager(address=('localhost', 10000), authkey=b'abracadabra')
	s = m.get_server()
	s.serve_forever()
	
if __name__ == '__main__':
	main()
