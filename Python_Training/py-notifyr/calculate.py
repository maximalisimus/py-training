#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pathlib
import json
from enum import Enum

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
	def JSONToSTR(data_json: dict) -> str:
		return json.dumps(data_json, indent=2)
	
	@staticmethod
	def STRToJSON(value: str) -> dict:
		json.loads(value)


def main():
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
	VirtX = {
			'left': 0,
			'center': 0,
			'right': 0
			}
	VirtY = {
			'top': 0,
			'center': 0,
			'bottom': 0
			}
	posx = PositionX.Right
	posy = PositionY.Top
	print(VirtX.get(posx.value,1))
	print(VirtY.get(posy.value,1))

if __name__ == '__main__':
	main()
