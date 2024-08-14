#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing.managers import BaseManager
from queue import Queue
import signal
import os
import sys
import threading
import base64
import tasks

import multiprocessing
import logging

import socket

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

handler = None
log_dict = dict()

class UserTimer:
	def __init__(self, link):
		self.link = link
		self.stop_timer = threading.Timer(1, lambda:self.link.stop_event.set())
	
	def start(self):
		print('Stop Server')
		#global handler, log_dict
		#handler.close()
		self.stop_timer.start()

def main():
	#client_server = ClientServer()
	#client_server.TestConnected('localhost', 10000)
	#print(client_server.is_server)
	#del client_server
	
	'''
	# '%(asctime)s - %(levelname)s - %(module)s - %(message)s'
	# '[%(asctime)s %(levelname)s/%(processName)s] %(message)s'
	# "[%(asctime)s %(levelname)s/$(name)s/%(module)s/%(processName)s] %(message)s"
	#
	logging.basicConfig(level=logging.INFO, filename=str('./log.log'),filemode="a",
						format="[%(asctime)s %(levelname)s/%(processName)s] %(message)s")
	# style - '%', '{', or '$' 
	## logging.Formatter('{asctime} {name} {levelname:8s} {message}', style='{')
	## logging.Formatter('$asctime $name ${levelname} $message', style='$')
	# datefmt='%m/%d/%Y %I:%M:%S %p'
	# datefmt='%d/%m/%Y %H:%M:%S'
	logger = logging.getLogger()
	logger.setLevel(logging.INFO) # DEBUG INFO WARNING ERROR CRITICAL
	# logger.debug(f"")
	# logger.error(f"")
	# logger.info(f"")
	# logger.warning(f"")
	# logger.critical(f"")
	
	
	1)
	import logging
	MYVAR = 'Jabberwocky'
	class ContextFilter(logging.Filter):
		"""
		This is a filter which injects contextual information into the log.
		"""
		def filter(self, record):
			record.MYVAR = MYVAR
			return True
	
	FORMAT = '%(MYVAR)s %(asctime)s - %(levelname)s - %(message)s'
	logging.basicConfig(format=FORMAT, datefmt='%d/%m/%Y %H:%M:%S')
	
	logger = logging.getLogger(__name__)
	logger.addFilter(ContextFilter())
	logger.warning("'Twas brillig, and the slithy toves")
	# Jabberwocky 24/04/2013 20:57:31 - WARNING - 'Twas brillig, and the slithy toves
	
	
	2)
	import logging
	logger = logging.LoggerAdapter(logging.getLogger(__name__), {'MYVAR': 'Jabberwocky'})
	FORMAT = '%(MYVAR)s %(asctime)s - %(levelname)s - %(message)s'
	logging.basicConfig(format=FORMAT, datefmt='%d/%m/%Y %H:%M:%S')
	logger.warning("'Twas brillig, and the slithy toves")
    
    
    3)
    import logging
    logger = logging.getLogger(__name__)
    FORMAT = '%(MYVAR)s %(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=FORMAT, datefmt='%d/%m/%Y %H:%M:%S')
    logger.warning("'Twas brillig, and the slithy toves", extra={'MYVAR': 'Jabberwocky'})
    
    # Поскольку MYVAR практически постоянен, LoggerAdapter подход требует меньше кода, чем Filter подход в вашем случае.
    
    # Заимствуя комментарий выше, я обнаружил, что самый простой способ сделать это, 
    # когда переменная статична для всех записей журнала, - просто включить ее в сам форматер:
    FORMAT = '{} %(asctime)s - %(levelname)s - %(message)s'.format(MYVAR)
    
	'''
	
	'''
	global handler, log_dict
	handler = logging.FileHandler('./log.log') # args.logfile
	formatter = logging.Formatter("[%(asctime)s %(levelname)s/%(processName)s] %(message)s", datefmt='%d/%m/%Y %H:%M:%S')
	handler.setFormatter(formatter)
	logger = multiprocessing.get_logger()
	logger.addHandler(handler)
	logger.setLevel(logging.DEBUG)
	#log_dict['err_logger'] = multiprocessing.get_logger()
	#log_dict['err_logger'].addHandler(handler)
	#log_dict['err_logger'].setLevel(logging.ERROR)
	
	#log_dict['crit_logger'] = multiprocessing.get_logger()
	#log_dict['crit_logger'].addHandler(handler)
	#log_dict['crit_logger'].setLevel(logging.CRITICAL)
	'''
	
	signal.signal(signal.SIGTERM, exit_handler)
	print(os.getpid())
	task = tasks.Task()
	#queue = Queue()
	#QueueManager.register('GetQueue', callable=lambda:queue)
	QueueManager.register('GetTasks', callable=lambda:task)
	qmanager = QueueManager(address=('localhost', 10000), authkey=b'abracadabra')
	# multiprocessing.managers.Server
	s = qmanager.get_server()
	#stop_timer = threading.Timer(1, lambda:s.stop_event.set())
	stop_timer = UserTimer(s)
	QueueManager.register('stop', callable=lambda:stop_timer.start())
	task.put(os.getpid())
	s.serve_forever()
	#handler.close()
	
if __name__ == '__main__':
	main()
