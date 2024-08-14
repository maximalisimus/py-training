#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing.managers import BaseManager
import time
import base64

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

class QueueManager(BaseManager):
	pass

def main():
	#QueueManager.register('GetQueue')
	QueueManager.register('GetTasks')
	m = QueueManager(address=('localhost', 10000), authkey=b'neabracadabra')
	connect = False
	try:
		m.connect()
		connect = True
	except:
		connect = False
	if connect:
		#queue = m.GetQueue()
		task = m.GetTasks()
		#'''
		server_pid = task.get(0)
		print('server_pid:', server_pid)
		print(task.qsize())
		if not task.empty():
			print(task.get())
			task.task_done()
		else:
			print('Queue is empty!')
		print(task.qsize())
		#'''
		'''
		data = {
				'position_x': 'right',
				'position_y': 'bottom',
				'Width': 394,
				'Height': 86,
				'Left': 1004,
				'Top': 645
				}
		index = task.put(data)
		#data2 = task.get(task.qsize()-1)
		#print(data2)
		task_list = task.copy()
		print(task_list)
		time.sleep(10)
		task.remove(data)
		task_list = task.copy()
		print(task_list)
		'''
	
if __name__ == '__main__':
	main()
