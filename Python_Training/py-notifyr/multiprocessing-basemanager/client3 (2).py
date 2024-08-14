#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing.managers import BaseManager
import time
import base64

import socket

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

class Boolean:
	
	@classmethod
	def verify_bool(cls, value):
		if type(value) != bool:
			raise TypeError('Enter the boolean!')
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return getattr(instance, self.name)

	def __set__(self, instance, value: str):
		self.verify_bool(value)
		setattr(instance, self.name, value)

class Strings:
	
	@classmethod
	def verify_str(cls, value):
		if type(value) != str:
			raise TypeError('Enter the string!')
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return getattr(instance, self.name)

	def __set__(self, instance, value: str):
		self.verify_str(value)
		setattr(instance, self.name, value)

class Integer:
	
	@classmethod
	def verify_int(cls, value):
		if type(value) != int:
			raise TypeError('Enter the integer!')
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return getattr(instance, self.name)

	def __set__(self, instance, value: int):
		self.verify_int(value)
		setattr(instance, self.name, value)

class ClientServer:
	
	DEBUG = Boolean()
	connected = Boolean()
	is_server = Boolean()
	data_out = Strings()
	
	def __init__(self):
		self.is_server = False
		self.connected = False
		self.data_out = ''
		self.DEBUG = False
	
	def TestConnected(self, address, port):
		s = socket.socket()
		self.connected = False
		try:
			s.connect((address, port))
			self.connected = True
			self.is_server = False
		except Exception as e:
			#print("something's wrong with %s:%d. Exception is %s" % (address, port, e))
			self.connected = False
			self.is_server = True
		finally:
			s.close()
		if self.connected:
			self.is_server = False
		else:
			self.is_server = True

def main():
	client_server = ClientServer()
	client_server.TestConnected('localhost', 10000)
	print(client_server.is_server)
	#del client_server
	
	#QueueManager.register('GetQueue')
	QueueManager.register('GetTasks')
	QueueManager.register('stop')
	m = QueueManager(address=('localhost', 10000), authkey=b'abracadabra')
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
