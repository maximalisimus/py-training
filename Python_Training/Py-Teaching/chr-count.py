#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def main():
	text = 'Добро - пожаловать!'
	keys = list(set(list(text.replace(' ', ''))))
	values = list(map(lambda x: text.replace(' ', '').count(x), keys))
	alpha_count = dict(zip(keys, values))
	#alpha_count = dict(zip(list(set(list(text.replace(' ', '')))), list(map(lambda x: text.replace(' ', '').count(x), list(set(list(text.replace(' ', ''))))))))
	#print(alpha_count)
	for k, v in alpha_count.items():
		print(f"\t{k}: {v}")

if __name__ == '__main__':
	main()
