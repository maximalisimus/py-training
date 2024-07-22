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
	QueueManager.register('stop')
	m = QueueManager(address=('localhost', 10000), authkey=Defaults.access_key)
	connect = False
	try:
		m.connect()
		connect = True
	except:
		connect = False
	if connect:
		'''
		task = m.GetTasks()
		for item in task.lists():
			if item['position_y'] == 'bottom':
				print(item)
		time.sleep(20)
		print(f"qsize = {task.qsize()}")
		print(f"empty = {task.empty()}")
		print(f"full = {task.full()}")
		print(task.lists())
		'''
		task = m.GetTasks()
		server_pid = task.get(0)
		print('server_pid:', server_pid)
		m.stop()
	
if __name__ == '__main__':
	main()
