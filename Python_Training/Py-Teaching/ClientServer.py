#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pathlib
import platform
import json
from enum import Enum
import socket
import multiprocessing
import time

class NoValue(Enum):

	def __repr__(self):
		return f"{self.__class__}: {self.name}"
	
	def __str__(self):
		return f"{self.name}"
	
	def __call__(self):
		return f"{self.value}"

class Weight(NoValue):
	normal = 'normal'
	bold = 'bold'
	
	@classmethod
	def GetWeightValue(cls, weight: str):
		for x in cls:
			if weight == x.value:
				return x
		return None

	@classmethod
	def GetWeightName(cls, pos):
		for x in cls:
			if os == x:
				return x
		return None

class PositionX(NoValue):
	Left = 'left'
	Right = 'right'
	Center = 'center'
	
	@classmethod
	def GetPosValue(cls, pos: str):
		for x in cls:
			if pos == x.value:
				return x
		return None

	@classmethod
	def GetPosName(cls, pos):
		for x in cls:
			if os == x:
				return x
		return None

class PositionY(NoValue):
	Top = 'top'
	Center = 'center'
	Bottom = 'Bottom'

	@classmethod
	def GetPosValue(cls, pos: str):
		for x in cls:
			if pos == x.value:
				return x
		return None

	@classmethod
	def GetPosName(cls, pos):
		for x in cls:
			if os == x:
				return x
		return None

class SockFName:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return f"clientserver.sock"

class FilesMeta(type):
	
	def __init__(cls, *args, **kwargs):
		super().__init__(*args, **kwargs)
	
	@property
	def socket_file(cls):
		return cls.ConfigDir.joinpath(cls.SockFileName)
	
	@property
	def ConfigDir(cls):
		if platform.system() == 'Linux':
			return pathlib.Path.home().joinpath('.config').joinpath('client-server')
		elif  platform.system() == 'Windows':
			return pathlib.Path.home().joinpath('AppData').joinpath('Roaming').joinpath('client-server')
		else:
			return pathlib.Path.home().joinpath('.config').joinpath('client-server') 

	@property
	def SockFileName(cls):
		return f"clientserver.sock"


class Files(metaclass=FilesMeta):
	
	@classmethod
	def CreateClientServer(cls):
		client_and_server = ClientServer()
		if not cls.socket_file.exists():
			client_and_server.set_free_port(cls.socket_file)
			del client_and_server
			client_and_server = ClientServer()
			client_and_server.set_free_port(cls.socket_file)
		else:
			client_and_server.set_free_port(cls.socket_file)
		return client_and_server
	
	@staticmethod
	def read_write_json(jfile, typerw, data = dict(), indent: int = 2):
		''' The function of reading and writing JSON objects. '''
		file_save = pathlib.Path(str(jfile)).resolve()
		file_save.parent.mkdir(parents=True,exist_ok=True)
		with open(str(file_save), typerw) as fp:
			if 'r' in typerw:
				data = json.load(fp)
				return data
			else:
				json.dump(data, fp, indent=indent)
	
	@staticmethod
	def JSONToSTR(data_json: dict) -> str:
		return json.dumps(data_json, indent=2)
	
	@staticmethod
	def STRToJSON(value: str) -> dict:
		return json.loads(value)

class HostName:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return 'localhost'

class SocketFullName:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return Files.ConfigDir.joinpath(Files.SockFileName)

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

class ClientServer:
	
	DEBUG = Boolean()
	connected = Boolean()
	is_server = Boolean()
	data_out = Strings()
	port = 5007
	host = HostName()

	def __init__(self):
		self.is_server = False
		self.connected = False
		self.data_out = ''
		self.DEBUG = False

	def __str__(self):
		return self.data_out

	def __repr__(self):
		return f"{self.__class__.__name__}:\n\t" +\
				f"is_server: {self.is_server}\n\t" +\
				f"connected: {self.connected}\n\t" +\
				f"data_out: {self.data_out}\n\t" +\
				f"DEBUG: {self.DEBUG}\n\t"

	def set_free_port(self, socket_file):
		socketfile = pathlib.Path(str(socket_file)).resolve()
		if not socketfile.exists():
			socketfile.parent.mkdir(mode=0o755, parents=True,exist_ok=True)
			self.find_free_port()
			port_dict = {'port': self.get_port()}
			Files.read_write_json(socketfile, 'w', port_dict)
		else:
			port_dict = Files.read_write_json(socketfile, 'r')
			if port_dict.get('port', '') != '' and type(port_dict.get('port', '')) == int:
				self.set_port(port_dict.get('port', ''))

	@classmethod
	def find_free_port(cls):
		with socket.socket() as s:
			s.bind(('', 0))            # Bind to a free port provided by the host.
			cls.set_port(s.getsockname()[1])  # Return the port number assigned.
	
	@classmethod
	def get_host(cls):
		return cls.host
	
	@classmethod
	def get_port(cls):
		return cls.port
	
	@classmethod
	def set_port(cls, value):
		cls.port = value
	
	def ReceiveData(self, size_data: int, host: str = 'localhost', port: int = 10000):
		msg_close = 'fine'.encode('utf-8')
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if self.DEBUG:
			print('Start client')
		try:
			sock.settimeout(2)
			sock.connect((host, port))
			sock.settimeout(None)
			self.connected = True
			self.data_out = ''
			if self.DEBUG:
				print('Client connect')
			self.is_server = False
			#while True:
			data = sock.recv(size_data)
			#if not data: break
			self.data_out = f"{self.data_out}{data.decode('utf-8')}"
			sock.sendall(msg_close)
			if self.DEBUG:
				print('Client sendall')
		except:
			self.connected = False
			self.is_server = False
			if self.DEBUG:
				print('Client Error')
		finally:
			sock.close()
			self.connected = False
			self.is_server = False
			if self.DEBUG:
				print('Client Close')

	def SendData(self, data_str: str, host: str = 'localhost', port: int = 10000):
		msg = ''
		msg_close = 'fine'.encode('utf-8')
		counter = len(msg_close)
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if self.DEBUG:
			print('Start server')
		try:
			message = data_str.encode('utf-8')
			sock.bind((host, port))
			sock.listen(1)
			conn, addr = sock.accept()
			self.connected = True
			self.is_server = True
			if self.DEBUG:
				print('Server connect')
			with conn:
				conn.sendall(message)
				data = conn.recv(counter)
				msg = data.decode('utf-8')
				if msg == 'fine':
					if self.DEBUG:
						print('Msg close')
					sock.close()
		except:
			self.connected = False
			self.is_server = True
			if self.DEBUG:
				print('Server error')
		finally:
			try:
				sock.close()
				if self.DEBUG:
					print('Server try close')
			except:
				if self.DEBUG:
					print('Server except close')
			self.connected = False
			self.is_server = True

def main():
	data = {
			'position_x': PositionX.Right.value,
			'position_y': PositionY.Top.value,
			'Width': 412,
			'Height': 92,
			'Left': 939,
			'Top': 15
			}
	data_str = Files.JSONToSTR(data)
	on_size = len(data_str.encode('utf-8'))
	clientserver = Files.CreateClientServer()
	clientserver.ReceiveData(on_size, clientserver.get_host(), clientserver.get_port())
	if not clientserver.is_server and clientserver.data_out != '':
		new_data = Files.STRToJSON(clientserver.data_out)
		print(new_data)
		exit(0)
	if not clientserver.connected:
		server = multiprocessing.Process(target=clientserver.SendData, args=(data_str, clientserver.get_host(), clientserver.get_port()))
		server.start()

if __name__ == '__main__':
	main()
