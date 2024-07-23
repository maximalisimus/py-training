'''A multi-producer, multi-consumer task.'''

import threading
import types
from time import monotonic as time

__all__ = ['Empty', 'Full', 'Task']

class Empty(Exception):
	'Exception raised by Task.get(block=0)/get_nowait().'
	pass

class Full(Exception):
	'Exception raised by Task.put(block=0)/put_nowait().'
	pass

class Task:

	def __init__(self, maxsize=0):
		self.maxsize = maxsize
		self._init(maxsize)
		
		# mutex must be held whenever the queue is mutating.  All methods
		# that acquire mutex must release it before returning.  mutex
		# is shared between the three conditions, so acquiring and
		# releasing the conditions also acquires and releases mutex.
		self.mutex = threading.Lock()
		
		# Notify not_empty whenever an item is added to the queue; a
		# thread waiting to get is notified then.
		self.not_empty = threading.Condition(self.mutex)
		
		# Notify not_full whenever an item is removed from the queue;
		# a thread waiting to put is notified then.
		self.not_full = threading.Condition(self.mutex)
		
		# Notify all_tasks_done whenever the number of unfinished tasks
		# drops to zero; thread waiting to join() is notified to resume
		self.all_tasks_done = threading.Condition(self.mutex)
		self.unfinished_tasks = 0

	def task_done(self):
		with self.all_tasks_done:
			unfinished = self.unfinished_tasks - 1
			if unfinished <= 0:
				if unfinished < 0:
					raise ValueError('task_done() called too many times')
				self.all_tasks_done.notify_all()
			self.unfinished_tasks = unfinished

	def join(self):
		with self.all_tasks_done:
			while self.unfinished_tasks:
				self.all_tasks_done.wait()

	def qsize(self):
		with self.mutex:
			return self._qsize()

	def empty(self):
		with self.mutex:
			return not self._qsize()

	def full(self):
		with self.mutex:
			return 0 < self.maxsize <= self._qsize()

	def put(self, item, block: bool = True, timeout=None):
		with self.not_full:
			if self.maxsize > 0:
				if not block:
					if self._qsize() >= self.maxsize:
						raise Full
				elif timeout is None:
					while self._qsize() >= self.maxsize:
						self.not_full.wait()
				elif timeout < 0:
					raise ValueError("'timeout' must be a non-negative number")
				else:
					endtime = time() + timeout
					while self._qsize() >= self.maxsize:
						remaining = endtime - time()
						if remaining <= 0.0:
							raise Full
						self.not_full.wait(remaining)
			self._put(item)
			self.unfinished_tasks += 1
			self.not_empty.notify()
			return self._qsize()-1

	def delete(self, index: int = -1, block: bool = True, timeout=None):
		with self.not_empty:
			if not block:
				if not self._qsize():
					raise Empty
			elif timeout is None:
				while not self._qsize():
					self.not_empty.wait()
			elif timeout < 0:
				raise ValueError("'timeout' must be a non-negative number")
			else:
				endtime = time() + timeout
				while not self._qsize():
					remaining = endtime - time()
					if remaining <= 0.0:
						raise Empty
					self.not_empty.wait(remaining)
			item = self._del(index)
			self.not_full.notify()
			return item

	def put_nowait(self, item):
		return self.put(item, block=False)

	def get_nowait(self):
		return self.get(block=False)

	def _init(self, maxsize):
		self.queue = []

	def _qsize(self) -> int:
		return len(self.queue)

	def _put(self, item):
		self.queue.append(item)

	def _del(self, index: int):
		return self.queue.pop(index)

	def _search(self, value):
		try:
			return self.queue.index(value)
		except ValueError:
			return None

	def search(self, value, block: bool = True, timeout=None):
		with self.not_empty:
			if not block:
				if not self._qsize():
					raise Empty
			elif timeout is None:
				while not self._qsize():
					self.not_empty.wait()
			elif timeout < 0:
				raise ValueError("'timeout' must be a non-negative number")
			else:
				endtime = time() + timeout
				while not self._qsize():
					remaining = endtime - time()
					if remaining <= 0.0:
						raise Empty
					self.not_empty.wait(remaining)
			on_index = self._search(value)
			self.not_full.notify()
			return self.queue[on_index] if on_index != None else None

	def searchIndex(self, value, block: bool = True, timeout=None) -> int:
		with self.not_empty:
			if not block:
				if not self._qsize():
					raise Empty
			elif timeout is None:
				while not self._qsize():
					self.not_empty.wait()
			elif timeout < 0:
				raise ValueError("'timeout' must be a non-negative number")
			else:
				endtime = time() + timeout
				while not self._qsize():
					remaining = endtime - time()
					if remaining <= 0.0:
						raise Empty
					self.not_empty.wait(remaining)
			on_index = self._search(value)
			self.not_full.notify()
			return on_index

	def copy(self):
		return self.queue[:]

	def list(self):
		return self.queue

	def remove(self, item, block: bool = True, timeout=None):
		curr_index = self.searchIndex(item, block, timeout)
		self.delete(curr_index)			

	def set(self, item, index: int = -1, block: bool = True, timeout=None):
		if index == -1:
			curr_index = self.searchIndex(item, block, timeout)
		else:
			curr_index = index
		with self.not_full:
			if self.maxsize > 0:
				if not block:
					if self._qsize() >= self.maxsize:
						raise Full
				elif timeout is None:
					while self._qsize() >= self.maxsize:
						self.not_full.wait()
				elif timeout < 0:
					raise ValueError("'timeout' must be a non-negative number")
				else:
					endtime = time() + timeout
					while self._qsize() >= self.maxsize:
						remaining = endtime - time()
						if remaining <= 0.0:
							raise Full
						self.not_full.wait(remaining)
			self.queue[curr_index] = item

	def get(self, index: int = -1, block: bool = True, timeout=None):
		with self.not_empty:
			if not block:
				if not self._qsize():
					raise Empty
			elif timeout is None:
				while not self._qsize():
					self.not_empty.wait()
			elif timeout < 0:
				raise ValueError("'timeout' must be a non-negative number")
			else:
				endtime = time() + timeout
				while not self._qsize():
					remaining = endtime - time()
					if remaining <= 0.0:
						raise Empty
					self.not_empty.wait(remaining)
			item = self.queue[index]
			self.not_full.notify()
			return item

	__class_getitem__ = classmethod(types.GenericAlias)
