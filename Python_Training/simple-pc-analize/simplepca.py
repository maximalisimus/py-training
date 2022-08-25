#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A program for collecting information about a PC and writing it to a log file.

Artamonov Mikhail [https://github.com/maximalisimus]
maximalis171091@yandex.ru
# License: GPL3
"""

__author__ = 'Mikhail Artamonov'

try:
	from .version import version, progname
except ImportError:
	version = "2.0.0"
	progname = 'simplepca.exe'

__version__ = version

import os
import platform
import pathlib
import sys
import argparse
import subprocess
from datetime import datetime
import shutil
from enum import Enum

import win32api
import win32file

from win32com.client import GetObject

from colorama import init, Fore

from icmplib import ping
from icmplib.exceptions import NameLookupError, SocketPermissionError, SocketAddressError, ICMPSocketError

'''
$ python -m pip install setuptools virtualenv virtualenvwrapper-win --upgrade

## Example
$ lsvirtualenv
$ mkvirtualenv spca-env

$ pip install pyinstaller pywin32 pywin32-ctypes colorama icmplib

$ pyinstaller main.py

# --onefile — сборка в один файл, т.е. файлы .dll не пишутся.
# --windowed -при запуске приложения, будет появляться консоль.
# --noconsole — при запуске приложения, консоль появляться не будет.
# --icon=app.ico — добавляем иконку в окно.
# --paths — возможность вручную прописать путь к необходимым файлам, если pyinstaller
# не может их найти(например: --paths D:\python35\Lib\site-packages\PyQt5\Qt\bin)

$ pyinstaller --onefile --icon=apps.ico --paths .version simplepca.py

'''

PREFIX = pathlib.Path(sys.argv[0]).resolve().parent

exclude_users = ('All Users', 'Default', 'Default User', 
				'desktop.ini', 'Public', 'Все пользователи', 
				'Intel', 'IntelGraphicsProfiles', 'AMD')

programs_dir = ''
if platform.machine() == 'AMD64':
	programs_dir = ('udefrag-x64/',
				'smartmontools/bin64/')
else:
	programs_dir = ('udefrag-x86/',
				'smartmontools/bin')

cmds = ('chcp 1252',
		'udefrag.exe -a -v', 
		'smartctl -s on -a')

file_hosts = str(os.environ.get('SYSTEMDRIVE')) + '\Windows\System32\drivers\etc\hosts'

default_structure_file = 'structure.txt'

default_out_color: bool = True

def size_format(in_size):
	if in_size < 1000:
		return f"{in_size} B"
	elif 1000 <= in_size < 1000000:
		#return '%.1f' % float(in_size/1000) + ' KB'
		return f"{float(in_size/1000):.1f} KB"
	elif 1000000 <= in_size < 1000000000:
		#return '%.1f' % float(in_size/1000000) + ' MB'
		return f"{float(in_size/1000000):.1f} MB"
	elif 1000000000 <= in_size < 1000000000000:
		# return '%.1f' % float(in_size/1000000000) + ' GB'
		return f"{float(in_size/1000000000):.1f} GB"
	elif 1000000000000 <= in_size:
		#return '%.1f' % float(in_size/1000000000000) + ' TB'
		return f"{float(in_size/1000000000000):.1f} TB"

def OnWinmgmts(OnObject: str):
	root_winmgmts = GetObject("winmgmts:root\cimv2")
	on_root = root_winmgmts.ExecQuery("Select * from " + OnObject)
	return on_root

def GetCPUType():
	cpus = OnWinmgmts('Win32_Processor')
	for x in cpus:
		output = f"{str(x.Name).strip()}, L2CacheSize = {str(size_format(x.L2CacheSize)).strip()}, " + \
				f"L3CacheSize = {str(size_format(x.L3CacheSize)).strip()}, " + \
				f"Cores = {str(x.NumberOfCores).strip()}, Thread = {str(x.NumberOfLogicalProcessors).strip()}"
		yield output

def GetMemory():
	memory = OnWinmgmts('Win32_PhysicalMemory')
	for x in memory:
		yield f"{x.Name}: {str(x.PartNumber).strip()}, {str(x.Speed).strip()} MHz, {size_format(int(x.Capacity))}"

def GetVideoControllerInfo():
	videocontroller = OnWinmgmts('Win32_VideoController')
	for x in videocontroller:
		yield f"{str(x.Name).strip()}, {str(x.VideoModeDescription).strip()}"

def GetNetAdapter():
	netadapter = OnWinmgmts('Win32_NetworkAdapter')
	for x in netadapter:
		if x.PhysicalAdapter:
			yield f"{x.Name}, {x.MACAddress}, {x.AdapterType}" + \
				f", Enabled {x.NetEnabled}"

def FastOnePing(addr: str, count = 4, interval: float = 0.5, pocket_size: int = 64, timeout: float = 2, source: str = None):
	out_text = []
	try:
		host = ping(addr, count = count, interval = interval, payload_size = pocket_size, timeout = timeout, source = source)
	except NameLookupError:
		out_text.append(f"PING {addr} {pocket_size} bytes of data.\nReply from {addr}\nNot available...")
	except (SocketPermissionError, SocketAddressError, ICMPSocketError) as err:
		out_text.append(f'SocketPermissionError, SocketAddressError or ICMPSocketError: {str(type(err).__name__)}.')
	except:
		out_text.append(f'Unknown error. The error name: {str(type(err).__name__)}.')
	else:
		out_text.append(f"PING {addr} ({host.address}) {pocket_size} bytes of data.")
		rtts = map(lambda x: f"{x:.3f}", host.rtts)
		for item in rtts:
			out_text.append(f"{pocket_size} bytes from addr ({host.address}): time={item}")
		out_text.append(f"--- {addr} ping statistics ---")
		out_text.append(f"\t{host.packets_sent} packets transmitted, {host.packets_received} received, {int(host.packet_loss * 100)}% packet loss")
		out_text.append(f"Aproximate rount trip times in milli-seconds:")
		out_text.append(f"\tMinimum = {host.min_rtt}ms, Maximum = {host.max_rtt}ms, Average = {host.avg_rtt}ms, Jitter = {host.jitter}ms")
	yield '\n'.join(out_text)

def GetPrinters():
	printers = OnWinmgmts('Win32_Printer')
	for x in printers:
		yield f"{x.Name}".replace('\n', '').strip()

class NoValue(Enum):

	def __repr__(self):
		return f"{self.__class__}: {self.name}"
	
	def __str__(self):
		return f"{self.name}"
	
	def __call__(self):
		return f"{self.value}"

class TypeDisk(NoValue):
	def __init__(self, on_type: win32file = win32file.DRIVE_UNKNOWN, on_value: str = ''):
		self.on_type = on_type
		self.on_value = on_value
	Unknown = (win32file.DRIVE_UNKNOWN, "Unknown Drive type can't be determined.")
	Local = (win32file.DRIVE_FIXED, "Fixed Drive has fixed (nonremovable) media. This includes all hard drives, including hard drives that are removable.")
	USB = (win32file.DRIVE_REMOVABLE, "Removable Drive has removable media. This includes all floppy drives and many other varieties of storage devices.")
	Network = (win32file.DRIVE_REMOTE, "Remote Network drives. This includes drives shared anywhere on a network.")
	CDROM = (win32file.DRIVE_CDROM, "CDROM Drive is a CD-ROM. No distinction is made between read-only and read/write CD-ROM drives.")
	RAM = (win32file.DRIVE_RAMDISK, "RAMDisk Drive is a block of random access memory (RAM) on the local computer that behaves like a disk drive.")
	NO_ROOT = (win32file.DRIVE_NO_ROOT_DIR, "The root directory does not exist.")
	
	@classmethod
	def GetTypeDisk(cls, value: int):
		for item in cls:
			if item.on_type == value:
				return item
	
	def __call__(self):
		return f"{self.on_value}"

def ListofTypeDisk(onfilter: TypeDisk = TypeDisk.Local) -> tuple:
	print('Requesting information about disks in the system.')
	drives = win32api.GetLogicalDriveStrings().split('\x00')[:-1]
	out = []
	for device in drives:
		diskinfo = TypeDisk.GetTypeDisk(win32file.GetDriveType(device))
		if diskinfo == onfilter:
			out.append(device.replace('\\',''))
	return tuple(out)

def SplitPath(path1: str, path2: str) -> str:
	global PREFIX
	return str(pathlib.Path(PREFIX).joinpath(path1).joinpath(path2).resolve())

def list_users() -> tuple:
	print('Getting a list of system users.')
	global exclude_users
	p = pathlib.Path.home()
	username = p.name
	all_user = list(map(lambda x: x.name, list(p.parent.iterdir())))
	on_users = [x for x in all_user if not x in exclude_users]
	return tuple(on_users)

def GetUserName() -> str:
	p = pathlib.Path.home()
	user1 = p.name
	user2 = os.getlogin()
	return user1 if user1 == user2 else str(user1 + ' or ' + user2)

def GetPingList(onFile: str = '') -> tuple:
	global default_out_color
	if default_out_color:
		print(Fore.YELLOW + 'Loading a list of addresses for pings.' + Fore.RESET)
	else:
		print('Loading a list of addresses for pings.')
	if onFile == '':
		ping_file = str(pathlib.Path().cwd().joinpath('ping-list.txt').resolve())
	else:
		if pathlib.Path(onFile).exists():
			ping_file = str(pathlib.Path(onFile).resolve())
		else:
			ping_file = str(pathlib.Path().cwd().joinpath('ping-list.txt').resolve())
	list_ping = ''
	with open(ping_file, 'r') as f:
		list_ping = tuple(map(lambda x: x.replace('\n',''), f.readlines()))
	return list_ping

def GetDateTime(strFormat: str = "%d.%m.%Y-%H:%M:%S") -> str:
	dateTime = datetime.now()
	onDateTime = dateTime.strftime(strFormat)
	return onDateTime

def GetLogName(FormatSTR: str = "%d.%m.%Y-%H:%M:%S") -> str:
	outDateTime = GetDateTime(FormatSTR)
	log_file = 'Log_' + platform.node() + '_' + outDateTime.split('-')[0] + '.txt'
	return log_file

def MakeDirs(LogDirs: str):
	global default_out_color
	if default_out_color:
		print(Fore.CYAN + 'Creating subdirectories for logs.' + Fore.RESET)
	else:
		print('Creating subdirectories for logs.')
	p = pathlib.Path(LogDirs)
	if not p.exists():
		p.mkdir(parents=True)	

def GetQurter(onMonth: int) -> str:
	rez = int((onMonth-1)/3 + 1)
	quarter = {1: '1st-quarter',
				2: '2nd-quarter',
				3: '3rd-quarter',
				4: '4th-quarter'}
	return quarter[rez]

def GetQuarterName() -> str:
	on_date = GetDateTime('%Y')
	on_month = int(GetDateTime('%m'))
	quarter_name = GetQurter(on_month) + '-' + on_date
	return quarter_name

def GetFileConfig(on_file: str, default_file: str) -> str:
	if on_file != '':
		tmpfile = pathlib.Path().cwd().joinpath(on_file)
		if tmpfile.exists():
			return str(tmpfile.resolve())
		else:
			return str(pathlib.Path().cwd().joinpath(default_file).resolve())
	else:
		return str(pathlib.Path().cwd().joinpath(default_file).resolve())

class Arguments:
	
	def __getattr__(self, attrname):
		return None
	
	def __repr__(self):
		return f"{self.__class__}: \n\t(nohosts={self.nohosts}, \n\tnodiskinfo={self.nodiskinfo}, \n\tnoping={self.noping}, \n\tnoprinters={self.noprinters}. \n\tnodefrag={self.nodefrag}, \n\tnosmart={self.nosmart}, \n\tpingfile={self.pingfile}, \n\tmove={self.move})"

def GetHostData() -> str:
	global default_out_color
	if default_out_color:
		print(Fore.YELLOW + 'Analysis of the hosts file ...' + Fore.RESET)
	else:
		print('Analysis of the hosts file ...')
	global file_hosts
	host_data = ''
	with open(file_hosts, 'r') as f:
		host_data = f.readlines()
	data_host = '\n'.join([x.strip() for x in host_data if not '#' in x]).strip()
	return data_host

def WriteBaseInfo(LogFile: str, ListDisks: tuple, isHosts: bool = True, isDisks: bool = True):
		
	all_users = list_users()
	username = GetUserName()
	cpu_info = GetCPUType()
	video_info = GetVideoControllerInfo()
	on_memory = GetMemory()
	networks = GetNetAdapter()
	if isHosts: on_hosts = GetHostData()
		
	global default_out_color
	if default_out_color:
		print(Fore.RED + 'Writing basic PC information to a log file ...' + Fore.RESET)
	else:
		print('Writing basic PC information to a log file ...')
	
	with open(LogFile, 'w') as f:
		f.write(f'{datetime.now().strftime("%d.%m.%Y-%H:%M:%S")}\n')
		f.write(f"Architecture: {platform.architecture()}\n")
		f.write(f"Machine: {platform.machine()}\n")
		f.write(f"Users: {' '.join(all_users)}\n")
		f.write(f"User login: {username}\n")
		f.write(f"Network Name: {platform.node()}\n")
		f.write(f"Release: {platform.release()}\n")
		f.write(f"System: {platform.system()}\n")
		f.write(f"Version: {platform.version()}\n")
		f.write(f"Platform: {platform.platform()}\n")
		f.write(f"CPU: {platform.processor()}\n")
		f.write(f"CPU INFO: \n")
		for i in cpu_info:
			f.write(f"\t{i}\n")
		f.write('VideoCards:\n')
		for i in video_info:
			f.write(f"\t{i}\n")
		f.write('Memory:\n')
		for i in on_memory:
			f.write(f"\t{i}\n")
		f.write('Network adapters:\n')
		for i in networks:
			f.write(f"\t{i}\n")
		f.write('\n')
		if isHosts:
			f.write(f"File hosts:\n")
			f.write(on_hosts)
			f.write('\n\n')
		else:
			f.write('\n')
		if isDisks:
			f.write('Local disk information:\n')
			for disks in ListDisks:
				total, used, free = shutil.disk_usage("C:")
				f.write(f"\tDisk {disks}\n")
				f.write(f"\t\tTotal: {total // (2**30)} GiB\n")
				f.write(f"\t\tUsed: {used // (2**30)} GiB\n")
				f.write(f"\t\tFree: {free // (2**30)} GiB\n")
			f.write('\n')
			del total, used, free

def createParser():
	global progname
	parser = argparse.ArgumentParser(prog=progname,description='Simple PC Analysis')
	parser.add_argument ('-v', '--version', action='version', version=f'{progname}  {__version__}',  help='Version.')
	parser.add_argument ('-nh', '--nohosts', action='store_false', default=True,  help='Do not read and write data from the hosts file.')
	parser.add_argument ('-nd', '--nodiskinfo', action='store_false', default=True, help='Do not read or write computer disk sizes.')
	parser.add_argument ('-np', '--noping', action='store_true', default=False, help='Do not read or write ping data.')
	parser.add_argument ('-pn', '--noprinters', action='store_true', default=False, help='Do not list printers.')
	parser.add_argument ('-nf', '--nodefrag', action='store_true', default=False, help='Do not read and write disks fragmentation data.')
	parser.add_argument ('-ns', '--nosmart', action='store_true', default=False, help='Do not read or write S.M.A.R.T. disks data.')
	parser.add_argument("-pf", '--pingfile', dest="pingfile", metavar='PINGFILE', type=str, default='', help='A file with a list for ping addresses.')
	parser.add_argument ('-nc', '--nocolorout', action='store_false', default=True, help='Discolor informational messages.')
	parser.add_argument("-c", '--oncount', dest="oncount", metavar='COUNT', type=int, default=4, help='Number of echo requests to send.')
	parser.add_argument("-i", '--oninterval', dest="oninterval", metavar='INTERVAL', type=float, default=0.5, help='The interval in seconds between sending each packet.')
	parser.add_argument("-s", '--onsize', dest="onsize", metavar='SIZE', type=int, default=64, help='Send buffer size.')
	parser.add_argument("-S", '--srcaddr', dest="srcaddr", metavar='SRCADDR', type=str, default=None, help='Source address to use.')
	parser.add_argument("-t", '--ontimeout', dest="ontimeout", metavar='TIMEOUT', type=float, default=2, help='The maximum waiting time for receiving a reply in seconds.')
	return parser

def main():
	global programs_dir
	global cmds
	global default_out_color
	
	init()
	
	parser = createParser()
	subparsers = parser.add_subparsers(title='Logs',
										description='Change the log output folder.',
										help='commands')
	parser_a = subparsers.add_parser('edit', help='Changing the location of logs.')
	parser_a.add_argument ('-ndf', '--nodatayear', action='store_true', default=False, help='Do not sort log files by year.')
	parser_a.add_argument ('-nq', '--noqarter', action='store_true', default=False, help='Do not sort log files by quarters.')
	
	structure_file = GetFileConfig('', default_structure_file)

	with open(structure_file, 'r') as f:
		kabinets = list(map(lambda x: x.replace('\n',''), f.readlines()))
	del structure_file
	parser_a.add_argument('-move', choices=kabinets, help='Select the kabinet or departament.')
	
	args = Arguments()
	parser.parse_args(namespace=Arguments)
	
	local_disk = ListofTypeDisk()
	
	default_out_color = args.nocolorout
	
	datafolder = '' if args.nodatayear else str('Log-' + GetDateTime('%Y'))
	qarter = '' if args.noqarter else GetQuarterName()
	
	logfile = pathlib.Path().cwd().joinpath('Log').joinpath(datafolder).joinpath(qarter).joinpath(args.move if args.nodatayear else str(args.move + '-' + GetDateTime('%Y'))).joinpath(GetLogName()) if args.move != None else pathlib.Path().cwd().joinpath('Log').joinpath(datafolder).joinpath(qarter).joinpath(GetLogName())
	logfile = logfile.resolve()
	MakeDirs(str(logfile.parent))	
	
	WriteBaseInfo(logfile, local_disk, args.nohosts, args.nodiskinfo)
	
	p = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
	
	if default_out_color:
		print(Fore.CYAN + 'Request for extended PC information.' + Fore.RESET)
	else:
		print('Request for extended PC information.')
	
	sys.stdout.flush()
	p.stdin.write(cmds[0] + "\n")
	
	if not args.noprinters:
		if default_out_color:
			print(Fore.YELLOW + 'Getting a list of printers.' + Fore.RESET)
		else:
			print('Getting a list of printers.')
		lst_printers = GetPrinters()
	
	ping_list = ''
	if not args.noping:
		ping_list = GetPingList(args.pingfile)
		if default_out_color:
			print(Fore.YELLOW + 'Loading the address ping function.' + Fore.RESET)
		else:
			print('Loading the address ping function.')
		full_ping = tuple(map(lambda x: FastOnePing(x, args.oncount, args.oninterval, args.onsize, args.ontimeout, args.srcaddr), ping_list))
	
	if not args.nodefrag:
		if default_out_color:
			print(Fore.MAGENTA + 'Analysis of disks defragmentation ...' + Fore.RESET)
		else:
			print('Analysis of disks defragmentation ...')
		on_program = SplitPath(programs_dir[0], cmds[1])
		for disks in local_disk:
			print(f"\tAnalysis disk {disks}\ ...")
			on_run = on_program + ' ' + disks
			sys.stdout.flush()
			p.stdin.write(on_run + "\n")
	
	if not args.nosmart:
		if default_out_color:
			print(Fore.MAGENTA + 'Analysis of S.M.A.R.T. information about disks in the system.' + Fore.RESET)
		else:
			print('Analysis of S.M.A.R.T. information about disks in the system.')
		on_program = SplitPath(programs_dir[1], cmds[2])
		for disks in local_disk:
			print(f"\tAnalysis disk {disks}\ ...")
			on_run = on_program + ' ' + disks
			sys.stdout.flush()
			p.stdin.write(on_run + "\n")
	
	# Close the 'stdin' process correctly
	p.stdin.close()
	
	# Free up some memory
	del local_disk
	del programs_dir
	del cmds
	
	out_data = ''
	if not args.nodefrag:
		# Delete a lot of 'analysis' lines:' from udefrag output
		data = p.stdout.read().split('\n')
		out_data = '\n'.join([x.strip() for x in data if not 'analysis:' in x]).strip()
		del data
	else:
		out_data = p.stdout.read()
	
	if default_out_color:
		print(Fore.RED + '\nWriting the received data to a log file ...' + Fore.RESET)
	else:
		print('\nWriting the received data to a log file ...')
	
	# write output data
	with open(logfile, 'a') as logfile:
		logfile.write(out_data)
		if not args.noprinters:
			logfile.write('\n\nList of printers:\n')
			for item in lst_printers:
				logfile.write('\t'+ item + '\n')
			logfile.write('\n')
		if not args.noping:
			logfile.write('\n\nList of pings:\n')
			if default_out_color:
				print(Fore.YELLOW + '\nPing of lists:' + Fore.RESET)
			else:
				print('\nPing of lists:')
			# ping_list
			for y in range(len(full_ping)):
				if default_out_color:
					print(Fore.CYAN + f'Ping of {ping_list[y]} ...' + Fore.RESET)
				else:
					print(f'Ping of {ping_list[y]} ...')
				for x in full_ping[y]:
					logfile.write(x + '\n')
				logfile.write('\n')
	
	# Close the 'Popen' process correctly
	p.terminate()
	p.kill()
	
	if default_out_color:
		print(Fore.GREEN + '\nThe system analysis has been successfully completed !' + Fore.RESET)
	else:
		print('\nThe system analysis has been successfully completed !')

if __name__ == '__main__':
	main()
