#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib

exclude_users = ['All Users', 'Default', 'Default User', 'desktop.ini', 'Public', 'Все пользователи', 'Intel', 'AMD']

def main():
	global exclude_users
	p = pathlib.Path.home()
	print(p.parts[-1], p.name)
	print(p.parent)
	all_users = list(map(lambda x: x.name, list(p.parent.iterdir())))
	#all_users = list(map(lambda x: x.name, list(p.parent.glob('*'))))
	pc_users = [x for x in all_users if not x in exclude_users]
	print(pc_users)

if __name__ == '__main__':
	main()
