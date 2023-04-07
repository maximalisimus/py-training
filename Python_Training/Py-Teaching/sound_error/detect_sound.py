#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyaudio
import pathlib

def main():
	log_file = pathlib.Path("./log.txt").resolve()
	p = pyaudio.PyAudio()
	info = p.get_host_api_info_by_index(0)
	numdevices = info.get('deviceCount')
	with open(log_file, 'w') as f:
		f.write(f"\n")
	for i in range(0, numdevices):
		if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
			print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
			with open(log_file, 'a') as f:
				f.write(f"Input Device id: {i}, - {p.get_device_info_by_host_api_device_index(0, i).get('name')}\n")

if __name__ == '__main__':
	main()
