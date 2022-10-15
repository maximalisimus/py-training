#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tasks

def main():
	'''
	t = tasks.Task(maxsize=5)
	print('Start:')
	print(f"qsize = {t.qsize()}")
	print(f"empty = {t.empty()}")
	print(f"full = {t.full()}")
	print('list of queue:', t.queue)
	lst = []
	for i in range(5):
		lst.append(t.put(i))
	print()
	print('Added elements:')
	print('put indexes:', lst)
	print('list of queue:', t.queue)
	print(f"qsize = {t.qsize()}")
	print(f"empty = {t.empty()}")
	print(f"full = {t.full()}")
	print()
	print('list of queue:', t.queue)
	print('get:',t.get())
	print('get(4):',t.get(4))
	print('get(0):',t.get(0))
	print('list of queue:', t.queue)
	print('delete:', t.delete())
	print('delete(1):',t.delete(1))
	print('list of queue:', t.queue)
	print()
	print('End operations to queue:')
	print(f"qsize = {t.qsize()}")
	print(f"empty = {t.empty()}")
	print(f"full = {t.full()}")
	print('list of queue:', t.queue)
	'''
	t = tasks.Task()
	print('Start:')
	print('list of queue:', t.queue)
	print(f"qsize = {t.qsize()}")
	print(f"empty = {t.empty()}")
	print(f"full = {t.full()}")
	t.put('Hello')
	t.put('World')
	t.put('!')
	print()
	print('Added Elements:')
	print('list of queue:', t.queue)
	print(f"qsize = {t.qsize()}")
	print(f"empty = {t.empty()}")
	print(f"full = {t.full()}")
	print()
	print("search('World'):", t.search('World'))
	print("search('Hello world!'):", t.search('Hello world!'))
	print("searchIndex('World'):", t.searchIndex('World'))
	print("searchIndex('Hello world!'):", t.searchIndex('Hello world!'))

if __name__ == '__main__':
	main()
