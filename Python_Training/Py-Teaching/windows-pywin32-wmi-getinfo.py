#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from win32com.client import GetObject

def GetCPUType():
	root_winmgmts = GetObject("winmgmts:root\cimv2")
	cpus = root_winmgmts.ExecQuery("Select * from Win32_Processor")
	return cpus[0].Name

def GetBaseBoardInfo():
	root_winmgmts = GetObject("winmgmts:root\cimv2")
	baseboard = root_winmgmts.ExecQuery("Select * from Win32_BaseBoard")
	return (baseboard[0].Version, baseboard[0].Product)

def GetVideoControllerInfo():
	root_winmgmts = GetObject("winmgmts:root\cimv2")
	videocontroller = root_winmgmts.ExecQuery("Select * from Win32_VideoController")
	return (videocontroller[0].Name, videocontroller[0].VideoModeDescription)

def main():
	print(GetCPUType())
	board_info = GetBaseBoardInfo()
	print(board_info[0], board_info[1])
	video_info = GetVideoControllerInfo()
	print(video_info[0], video_info[1])
	pass

if __name__ == '__main__':
	main()
