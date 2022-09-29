#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pathlib
import json
from enum import Enum
import socket
import multiprocessing
import time

connected = False
data_out = ''
# event = multiprocessing.Event()

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

class Files:
	
	@staticmethod
	def WriteJson(data_json: dict, file_json: str = 'object.json'):
		json_string = json.dumps(data_json, indent=2)
		with open(pathlib.Path(file_json).resolve(), "w") as fp:
			fp.write(json_string)

	@staticmethod
	def ReadJson(file_json: str = 'object.json') -> dict:
		data = ''
		with open(pathlib.Path(file_json).resolve(), "r") as fp:
			data = json.loads(fp.read())
		return data

	@staticmethod
	def JSONToSTR(data_json: dict) -> str:
		return json.dumps(data_json, indent=2)
	
	@staticmethod
	def STRToJSON(value: str) -> dict:
		json.loads(value)

def ReceiveData(size_data: int, host: str = 'localhost', port: int = 10000):
	global connected
	global data_out
	msg_close = 'fine'.encode('utf-8')
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print('Start client')
	try:
		sock.settimeout(2)
		sock.connect((host, port))
		sock.settimeout(None)
		connected = True
		data_out = ''
		print('Client connect')
		#while True:
		data = sock.recv(size_data)
		#if not data: break
		data_out += data.decode('utf-8')
		sock.sendall(msg_close)
		print('Client sendall')
	except:
		connected = False
		print('Client Error')
	finally:
		sock.close()
		connected = False
		print('Client Close')

def SendData(data_str: str, host: str = 'localhost', port: int = 10000):
	global connected
	msg = ''
	msg_close = 'fine'.encode('utf-8')
	counter = len(msg_close)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print('Start server')
	try:
		message = data_str.encode('utf-8')
		sock.bind((host, port))
		sock.listen(1)
		conn, addr = sock.accept()
		connected = True
		print('Server connect')
		with conn:
			conn.sendall(message)
			data = conn.recv(counter)
			msg = data.decode('utf-8')
			if msg == 'fine':
				print('Msg close')
				sock.close()
	except:
		connected = False
		print('Server error')
	finally:
		try:
			sock.close()
			print('Server try close')
		except:
			print('Server except close')
		connected = False	

def main():
	global connected
	global data_out
	data = {
			'screen_width': 1366,
			'screen_height': 768,
			'position_x': PositionX.Right.value,
			'position_y': PositionY.Top.value,
			'Width': 412,
			'Height': 92,
			'Left': 939,
			'Top': 15
			}
	print('Start')
	data_str = Files.JSONToSTR(data)
	on_size = len(data_str.encode('utf-8'))
	HOST = 'localhost'
	PORT = 5007
	ReceiveData(on_size, HOST, PORT)
	print(data_out)
	if not connected:
		print('Global code')
		server = multiprocessing.Process(target=SendData, args=(data_str, HOST, PORT))
		server.start()
	time.sleep(10)
	print('Fine')
	if server.is_alive():
		server.kill()
	

if __name__ == '__main__':
	main()
