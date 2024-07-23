#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import platform
import sys
import pathlib

__author__ = 'Mikhail Artamonov'
__description__ = 'Cross-platform graphical desktop notifications and reminders based on Tk/Tcl.'
__progname__ = str(pathlib.Path(sys.argv[0]).resolve().name)
__copyright__ = f"© The \"{__progname__}\". Copyright  by 2024."
__credits__ = ["Mikhail Artamonov"]
__license__ = "GPL3"
__version__ = "1.0.0"
__maintainer__ = "Mikhail Artamonov"
__status__ = "Production"
__date__ = '11.10.2022'
__modifed__ = '22.07.2024'

class Files:
	
	@staticmethod
	def read_write_file(onfile, typerw, data = ""):
		''' The function of reading and writing text files. '''
		file_save = pathlib.Path(str(onfile)).resolve()
		file_save.parent.mkdir(parents=True,exist_ok=True)
		with open(str(file_save), typerw) as fp:
			if 'r' in typerw:
				data = fp.read()
				return data
			else:
				fp.write(data)

class SystemdText:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return f"[Unit]\n" +\
				f"Description={__description__}\n" +\
				f"Wants=graphical.target\n" +\
				f"After=graphical.target\n\n" +\
				f"[Service]\n" +\
				f"Type=simple\n" +\
				f"RemainAfterExit=no\n" +\
				f"ExecStart={str(pathlib.Path(__progname__).name).split('.')[0]} daemon -run\n" +\
				f"ExecStop={str(pathlib.Path(__progname__).name).split('.')[0]} daemon -stop\n" +\
				f"ExecReload={str(pathlib.Path(__progname__).name).split('.')[0]} daemon -restart\n\n" +\
				f"[Install]\n" +\
				f"WantedBy=multi-user.target"

class SystemdConfig:
	
	config = SystemdText()
	
	def __repr__(self):
		return f"{self.__class__}: {self.config}"
	
	def __str__(self):
		return f"{self.config}"
	
	def __call__(self):
		return f"{self.config}"

class AuthorInfo:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return f"Author: {__author__}\nProgname: {__progname__}\nVersion: {__version__}\n" + \
			f"Description: {__description__}\n" +\
			f"Date of creation: {__date__}\nLast modified date: {__modifed__}\n" + \
			f"License: {__license__}\nCopyright: {__copyright__}\nCredits: {__credits__}\n" + \
			f"Maintainer: {__maintainer__}\nStatus: {__status__}\n"

class Author:
	
	Info = AuthorInfo()

	def __repr__(self):
		return f"{self.__class__}: {self.Info}"
	
	def __str__(self):
		return f"{self.Info}"
	
	def __call__(self):
		return f"{self.Info}"

class Base:
	
	__slots__ = ['__dict__']
		
	def __init__(self):
		self.except_list = []
	
	def __str__(self):
		''' For STR Function output paramters. '''
		return '\t' + '\n\t'.join(f"{x}: {getattr(self, x)}" for x in dir(self) if not x in self.except_list and '__' not in x)
	
	def __repr__(self):
		''' For Debug Function output paramters. '''
		return f"{self.__class__}:\n\t" + \
				'\n\t'.join(f"{x}: {getattr(self, x)}" for x in dir(self) if not x in self.except_list and '__' not in x)

class Arguments(Base):
	''' The class of the set of input parameters. '''
	
	def __init__(self, *args, **kwargs):
		super(Arguments, self).__init__()
		self.except_list.append('except_list')
		self.except_list.append('Reset')
		self.except_list.append('ApplyTheme')
		self.except_list.append('SaveTheme')
		self.except_list.append('CreateDefaultConfig')
		self.except_list.append('save')
		self.except_list.append('load')
		self.except_list.append('reset')
		self.except_list.append('output')
		self.except_list.append('FormPos')
		self.except_list.append('TempPos')
		self.except_list.append('SocketFormPos')
		self.except_list.append('ThemeDict')
		self.except_list.append('isTheme')
		self.Title = args[0] if len(args) >= 1 else kwargs.get('Title','Apps')
		self.Message = args[1] if len(args) >= 2 else kwargs.get('Message','Info!')
		self.OnTime = args[2] if len(args) >= 3 else kwargs.get('OnTime', 5000)
		self.isTimer = args[3] if len(args) >= 4 else kwargs.get('isTimer',True)
		self.icon = args[4] if len(args) >= 5 else kwargs.get('icon','None')
		self.TFFamily = args[5] if len(args) >= 6 else kwargs.get('TFFamily','Arial')
		self.TFSize = args[6] if len(args) >= 7 else kwargs.get('TFSize', 12)
		self.TFWeight = args[7] if len(args) >= 8 else kwargs.get('TFWeight','bold')
		self.TFUnderline = args[8] if len(args) >= 9 else kwargs.get('TFUnderline', 0)
		self.TFSlant = args[9] if len(args) >= 10 else kwargs.get('TFSlant','roman')
		self.TFOverstrike = args[10] if len(args) >= 11 else kwargs.get('TFOverstrike',0)
		self.TitleFG = args[11] if len(args) >= 12 else kwargs.get('TitleFG','black')
		self.BFFamily = args[12] if len(args) >= 13 else kwargs.get('BFFamily','Arial')
		self.BFSize = args[13] if len(args) >= 14 else kwargs.get('BFSize', 12)
		self.BFWeight = args[14] if len(args) >= 15 else kwargs.get('BFWeight','normal')
		self.BFUnderline = args[15] if len(args) >= 16 else kwargs.get('BFUnderline', 0)
		self.BFSlant = args[16] if len(args) >= 17 else kwargs.get('BFSlant','roman')
		self.BFOverstrike = args[17] if len(args) >= 18 else kwargs.get('BFOverstrike', 0)
		self.BG = args[18] if len(args) >= 19 else kwargs.get('BG','#FFFADD')
		self.BodyFG = args[19] if len(args) >= 20 else kwargs.get('BodyFG','black')
		self.scale = args[20] if len(args) >= 21 else kwargs.get('scale', '1,1')
		self.PosX = args[21] if len(args) >= 22 else kwargs.get('PosX', 'right')
		self.PosY = args[22] if len(args) >= 23 else kwargs.get('PosY', 'top')
		self.Alpha = args[23] if len(args) >= 24 else kwargs.get('Alpha', 1.0)
		self.MoveX = args[24] if len(args) >= 25 else kwargs.get('MoveX', 0)
		self.MoveY = args[25] if len(args) >= 26 else kwargs.get('MoveY', 0)
		self.Relative = args[26] if len(args) >= 27 else kwargs.get('Relative', True)
		self.Topmost = args[27] if len(args) >= 28 else kwargs.get('Topmost', False)
		self.save = args[28] if len(args) >= 29 else kwargs.get('save', False)
		self.load = args[29] if len(args) >= 30 else kwargs.get('load', False)
		self.reset = args[30] if len(args) >= 31 else kwargs.get('reset', False)
		self.CloseIcon = args[31] if len(args) >= 32 else kwargs.get('CloseIcon', 'default')
		self.Theme = args[32] if len(args) >= 33 else kwargs.get('Theme', '')
		self.isTheme = args[33] if len(args) >= 34 else kwargs.get('isTheme', False)
		self.output = args[34] if len(args) >= 35 else kwargs.get('output', '')
		self.Style = args[35] if len(args) >= 36 else kwargs.get('Style', 'standart')
		self.ScaleClose = args[36] if len(args) >= 37 else kwargs.get('ScaleClose', '1,1')
		self.distance = args[37] if len(args) >= 38 else kwargs.get('distance', 10)
		self.FormPos = dict()
		self.SocketFormPos = dict()
		self.TempPos = dict()
		self.ThemeDict = dict()
	
	def __getattr__(self, attrname):
		''' Access to a non-existent variable. '''
		return None

def createParser():
	
	dict_parser = dict()
	'''
	Кросс-платформенные графические уведомления и напоминания на рабочем столе на основе Tk/Tcl.
	Cross-platform graphical desktop notifications and reminders based on Tk/Tcl.
	'''
	parser = argparse.ArgumentParser(prog=__progname__,description='Cross-platform graphical desktop notifications and reminders based on Tk/Tcl.')
	parser.add_argument ('-V', '--version', action='version', version=f'{__progname__} {__version__}',  help='Version.')
	parser.add_argument ('-info', '--info', action='store_true', default=False, help='Information about the author.')
	
	dict_parser['parser'] = parser
	
	subparsers = parser.add_subparsers(title='Management', description='Management commands.', help='commands help.')
	
	dict_parser['subparsers'] = subparsers

	if  platform.system() == 'Windows':
		pass
	elif platform.system() == 'Linux':
		parser_systemd = subparsers.add_parser('systemd', help='Systemd management.')
		
		parser_systemd.add_argument ('-create', '--create', action='store_true', default=False, help='Create «pynotifyr.service».')
		parser_systemd.add_argument ('-delete', '--delete', action='store_true', default=False, help='Delete «pynotifyr.service».')
		parser_systemd.add_argument ('-status', '--status', action='store_true', default=False, help='Status «pynotifyr.service».')
		parser_systemd.add_argument ('-enable', '--enable', action='store_true', default=False, help='Enable «pynotifyr.service».')
		parser_systemd.add_argument ('-disable', '--disable', action='store_true', default=False, help='Disable «pynotifyr.service».')
		parser_systemd.add_argument ('-start', '--start', action='store_true', default=False, help='Start «pynotifyr.service».')
		parser_systemd.add_argument ('-stop', '--stop', action='store_true', default=False, help='Stop «pynotifyr.service».')
		parser_systemd.add_argument ('-reload', '--reload', action='store_true', default=False, help='Reload «pynotifyr.service».')
		parser_systemd.set_defaults(onlist='systemd')
		
		dict_parser['parser_systemd'] = parser_systemd
	parser_daemon = subparsers.add_parser('daemon', help='Daemon control.')
	
	parser_daemon.add_argument ('-start', '--start', action='store_true', default=False, help='Start daemon.')
	parser_daemon.add_argument('-run', '--run', action='store_true', default=False, help=argparse.SUPPRESS)
	parser_daemon.add_argument ('-stop', '--stop', action='store_true', default=False, help='Stop daemon.')
	parser_daemon.add_argument ('-restart', '--restart', action='store_true', default=False, help='Restart daemon.')
	parser_daemon.add_argument ('-kill', '--kill', action='store_true', default=False, help='Kill daemon.')
	parser_daemon.set_defaults(onlist='daemon')
	
	dict_parser['parser_daemon'] = parser_daemon
	
	# group1 = parser.add_argument_group('Parameters', 'Settings for the number of bans.')
	# group1.add_argument("-c", '--count', dest="count", metavar='COUNT', type=int, default=0, help='Help.')
	# dict_parser['group1'] = group1
	
	return dict_parser

def main(*argv):
	parser_dict = createParser()
	args = Arguments()
	if len(argv) > 0:
		parser_dict['parser'].parse_args(args=argv, namespace=Arguments)
	else:
		parser_dict['parser'].parse_args(namespace=Arguments)
	
	if args.info:
		print(Author.Info)
		sys.exit(0)
	
	

if __name__ == '__main__':
	main()
