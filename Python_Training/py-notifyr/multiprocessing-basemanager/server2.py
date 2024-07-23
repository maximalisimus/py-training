#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing.managers import BaseManager
import tasks
import signal
import os
import sys
import threading
import multiprocessing
import pathlib
import time
import base64

qmanager = ''

class CheckAccess:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return 'py-notifyr'

class Meta(type):
	
	def __init__(cls, *args, **kwargs):
		super().__init__(*args, **kwargs)
	
	@property
	def access_key(cls):
		return Texts.StrToBase(Texts.Access)
		
class Defaults(metaclass=Meta):
	
	pass

class Texts:
	
	Access = CheckAccess()
	
	@staticmethod
	def StrToBase(inputSTR: str):
		str_bytes = inputSTR.encode('utf-8')
		return base64.b64encode(str_bytes)
	
	@staticmethod
	def BaseToSTR(inputBase: str):
		data = base64.b64decode(inputBase)
		return data.decode('utf-8')

def exit_handler(signum, frame):
	global qmanager
	qmanager.shutdown()
	print('Exiting....')
	sys.exit(0)

class QueueManager(BaseManager):
	pass

def RunServer():
	signal.signal(signal.SIGTERM, exit_handler)
	#print(os.getpid())
	task = tasks.Task()
	QueueManager.register('GetTasks', callable=lambda:task)
	qmanager = QueueManager(address=('localhost', 10000), authkey=Defaults.access_key)
	s = qmanager.get_server()
	stop_timer = threading.Timer(1, lambda:s.stop_event.set())
	QueueManager.register('stop', callable=lambda:stop_timer.start())
	task.put(os.getpid())
	s.serve_forever()

def main():
	# https://docs-python.ru/standart-library/modul-threading-python/klass-thread-modulja-threading/
	# https://docs-python.ru/standart-library/paket-multiprocessing-python/funktsija-process-modulja-multiprocessing/
	server = multiprocessing.Process(target=RunServer, args=())
	server.start()
	server.join()
	
if __name__ == '__main__':
	main()
