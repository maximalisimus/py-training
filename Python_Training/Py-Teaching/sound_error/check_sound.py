#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import pathlib
import sys

import pyaudio
import os
import signal
import subprocess

log_file = pathlib.Path("./log.txt").resolve()

def callback(in_data, frame_count, time_info, status):
	pid = os.getpid()
	with open(log_file, 'a') as f:
		f.write(f"{pid}\n")
	return (in_data, pyaudio.paContinue)

device_index = 0
if len(sys.argv) >= 2:
	device_index = int(sys.argv[1])

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024,
                input_device_index=device_index, stream_callback=callback)

class MyForm:
	def __init__(self, master):
		self.master = master
		master.title("My Form")
		master.geometry("480x320+{}+{}".format(int(master.winfo_screenwidth()/2 - 480/2), int(master.winfo_screenheight()/2 - 320/2)))
		
		self.icon_file = pathlib.Path('./sound-icon_32.png').resolve()
		if self.icon_file.exists():
			icon = tk.PhotoImage(file=str(self.icon_file))
			master.iconphoto(True, icon)

		self.button_start = ttk.Button(master, text="Start")
		self.button_start.bind("<Button-1>", self.start_click)
		self.button_start.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=20, pady=20)

		self.button_stop = ttk.Button(master, text="Stop")
		self.button_stop.bind("<Button-1>", self.stop_click)
		self.button_stop.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=20, pady=20)
		stream.stop_stream()

	def start_click(self, event):
		#print("Start button clicked")
		stream.start_stream()
		pass

	def stop_click(self, event):
		#print("Stop button clicked")
		stream.stop_stream()
		pass

def main():
	root = tk.Tk()
	my_form = MyForm(root)
	root.mainloop()
	stream.close()
	p.terminate()

if __name__ == '__main__':
	main()
