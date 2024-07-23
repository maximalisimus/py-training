#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tasks

def main():
	'''
	task = tasks.Task()
	data = {
			'position_x': 'right',
			'position_y': 'top',
			'Width': 412,
			'Height': 92,
			'Left': 939,
			'Top': 15
			}
	index = task.put(data)
	print(f"qsize = {task.qsize()}")
	print(f"empty = {task.empty()}")
	print(f"full = {task.full()}")
	print('list of queue:', task.queue)
	data2 = data.copy()
	data2['position_y'] = 'bottom'
	index2 = task.put(data2)
	print()
	print(f"qsize = {task.qsize()}")
	print(f"empty = {task.empty()}")
	print(f"full = {task.full()}")
	print('list of queue:', task.queue)
	print()
	print(task.queue[0])
	print()
	task.delete(index2)
	print(f"qsize = {task.qsize()}")
	print(f"empty = {task.empty()}")
	print(f"full = {task.full()}")
	print('list of queue:', task.queue)
	print()
	print(task.queue[0])
	print(data)
	print()
	data = task.get(index)
	data['position_y'] = 'bottom'
	task.set(data, index)
	print(task.queue[0])
	print(data)
	print()
	print(f"qsize = {task.qsize()}")
	print(f"empty = {task.empty()}")
	print(f"full = {task.full()}")
	print('list of queue:', task.queue)
	print()
	task.delete(index)
	print()
	print(f"qsize = {task.qsize()}")
	print(f"empty = {task.empty()}")
	print(f"full = {task.full()}")
	print('list of queue:', task.queue)
	'''

if __name__ == '__main__':
	main()
