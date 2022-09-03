#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pathlib
import json
import configparser

PREFIX = pathlib.Path(sys.argv[0]).resolve().parent

def GetFileConfig(on_file: str):
	global PREFIX
	return PREFIX.joinpath(on_file)

def ReadConfig(File_Config: str = "English.json") -> dict:
	data = ''
	with open(GetFileConfig(File_Config), "r") as fp:
		data = json.load(fp)
	return data

def main():
	config = configparser.ConfigParser()
	if config.sections() == []:
		config.read(GetFileConfig('config.ini'))
	lng = str(GetFileConfig(f"{config['DEFAULT']['Language']}.json"))
	language = ReadConfig(lng)
	print(language['Device']['Local'])
	pass

if __name__ == '__main__':
	main()
