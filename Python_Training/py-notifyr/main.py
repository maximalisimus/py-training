#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pathlib
import json

class Files:
	
	@staticmethod
	def WriteJson(data_json: dict, file_json: str = 'object.json'):
		''' Write Json data in file '''
		with open(pathlib.Path(file_json).resolve(), "w") as fp:
			json.dump(data_json, fp, indent=2)

	@staticmethod
	def ReadJson(file_json: str = 'object.json') -> dict:
		''' Read Json Data from File '''
		data = ''
		with open(pathlib.Path(file_json).resolve(), "r") as fp:
			data = json.load(fp)
		return data

def main():
	pass
	#dark_theme = {'TitleBG': '#303030', 'TitleFG': 'white', 'BodyBG': '#303030', 'BodyFG': 'white', 'Alpha': 0.9}
	#light_theme = {'TitleBG': '#FFFADD', 'TitleFG': 'black', 'BodyBG': '#FFFADD', 'BodyFG': 'black', 'Alpha': 0.9}
	#Files.WriteJson(dark_theme, 'dark-theme.json')
	#Files.WriteJson(light_theme, 'light-theme.json')
	dark_theme = Files.ReadJson('dark-theme.json')
	light_theme = Files.ReadJson('light-theme.json')
	print(dark_theme)
	print(light_theme)

if __name__ == '__main__':
	main()
