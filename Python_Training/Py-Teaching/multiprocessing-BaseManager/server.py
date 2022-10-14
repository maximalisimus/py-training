#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing.managers import BaseManager
from queue import Queue
import signal
import os
import sys

qmanager = ''

def exit_handler(signum, frame):
	global qmanager
	qmanager.shutdown()
	print('Exiting....')
	sys.exit(0)

class QueueManager(BaseManager):
	pass

def main():
	signal.signal(signal.SIGTERM, exit_handler)
	print(os.getpid())
	queue = Queue()
	QueueManager.register('GetQueue', callable=lambda:queue)
	qmanager = QueueManager(address=('localhost', 10000), authkey=b'abracadabra')
	s = qmanager.get_server()
	s.serve_forever()
	
if __name__ == '__main__':
	main()
