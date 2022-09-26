#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pathlib
from os import mkfifo
import json
from enum import Enum

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

def main():
	data = {
			'screen_width': 1366,
			'screen_height': 768,
			'position_x': PositionX.Right.value,
			'position_y': PositionY.Top.value,
			'Width': 200,
			'Height': 100,
			'Top': 15,
			'Left': 960
			}
	FIFO = pathlib.Path(sys.argv[0]).parent.joinpath('pipe1').resolve()
	if not FIFO.exists():
		mkfifo(FIFO)
	Files.WriteJson(data, FIFO)
	print('Send dict on FIFO:', data)

if __name__ == '__main__':
	main()
