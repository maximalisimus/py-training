#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import win32com.client
import pathlib
import os
import sys
import argparse

# pip install pyinstaller pywin32 pywin32-ctypes

# pyinstaller --onefile --icon=image/apps.ico pyicon.py

__author__ = 'Mikhail Artamonov'
__progname__ = str(pathlib.Path(sys.argv[0]).resolve().name)
__years__ = '2024'
__copyright__ = f"The \"{__progname__}\". Copyright  by {__years__}."
__credits__ = ["Mikhail Artamonov"]
__license__ = "GPL3"
__version__ = "1.0.0"
__maintainer__ = "Mikhail Artamonov"
__email__ = "maximalisimus121@mail.ru"
__status__ = "Production"
__date__ = '11.04.2024'
__modifed__ = '12.04.2024'

infromation = f"Author: {__author__}\nProgname: {__progname__}\nVersion: {__version__}\n" + \
			f"Date of creation: {__date__}\nLast modified date: {__modifed__}\n" + \
			f"License: {__license__}\nCopyright: {__copyright__}\nCredits: {__credits__}\n" + \
			f"Maintainer: {__maintainer__}\nStatus: {__status__}\n" + \
			f"E-Mail: {__email__}"

class Arguments:
	''' Class «Arguments».
	
		Info: A class designed to store command-line values 
				by entering parameters through the «Argparse» module.
		
		Variables: All parameters are entered using the «createParser()» 
					method.
		
		Methods: 
			__getattr__(self, attrname):
				Access to a non-existent variable.
				Used when trying to get a parameter that does not exist. 
				In this case, «None» is returned to the user, instead 
				of an error.
			
			__str__(self):
				For STR Function output paramters.
			
			__repr__(self):
				For Debug Function output paramters.
	'''
	
	__slots__ = ['__dict__']
	
	def __getattr__(self, attrname):
		''' Access to a non-existent variable. '''
		return None

	def __str__(self):
		''' For STR Function output paramters. '''
		except_list = ['']
		#return '\t' + '\n\t'.join(tuple(map(lambda x: f"{x}: {getattr(self, x)}" if not x in except_list else f"", tuple(filter( lambda x: '__' not in x, dir(self))))))
		return '\t' + '\n\t'.join(f"{x}: {getattr(self, x)}" for x in dir(self) if not x in except_list and '__' not in x)
	
	def __repr__(self):
		''' For Debug Function output paramters. '''
		except_list = ['']
		return f"{self.__class__}:\n\t" + \
				'\n\t'.join(f"{x}: {getattr(self, x)}" for x in dir(self) if not x in except_list and '__' not in x)
				#'\n\t'.join(tuple(map(lambda x: f"{x}: {getattr(self, x)}" if not x in except_list else f"", tuple(filter( lambda x: '__' not in x, dir(self))))))

def createParser():
	''' The function of creating a parser with a certain hierarchy 
		of calls. Returns the parser itself and the sub-parser, 
		as well as groups of parsers, if any. '''
	dict_parser = dict()
	parser = argparse.ArgumentParser(prog=__progname__,description='Info.')
	parser.add_argument ('-v', '--version', action='version', version=f'{__progname__} {__version__}',  help='Version.')
	parser.add_argument ('-info', '--info', action='store_true', default=False, help='Information about the author.')
	
	dict_parser['parser'] = parser
	
	parser.add_argument("-inpath", '--inpath', dest="inpath", metavar='INPATH', type=str, default='./shortcuts', help='Input shortcut directory (default: "./shortcuts").')
	parser.add_argument("-n", '--name', dest="name", metavar='NAME', type=str, default='example', help='Label name (requeired, default: "example").')
	parser.add_argument("-t", '--target', dest="target", metavar='TARGET', type=str, default='', help='Target link (requeired).')
	parser.add_argument("-w", '--working', dest="working", metavar='WORKING', type=str, default='', help='The working directory.')
	parser.add_argument("-icon", '--icon', dest="icon", metavar='ICON', type=str, default='', help='The icon of the shortcut.')
	parser.add_argument("-a", '--arguments', dest="arguments", metavar='ARGUMENTS', type=str, default='', help='Label arguments.')
	parser.add_argument ('-u', '--url', action='store_true', default=False, help='The type of shortcut the web address. The default is the shortcut.')
	parser.add_argument ('-e', '--example', action='store_true', default=False, help='Examples.')
	
	return dict_parser

def main():
	
	global infromation
	
	parser_dict = createParser()
	args = Arguments()

	parser_dict['parser'].parse_args(namespace=Arguments)
	
	if args.info:
		print(infromation)
		sys.exit(0)
	
	if args.example:
		print("Shortcut:")
		fname = f"{__progname__}".split(".")[0]
		print(f"\t{fname} -n GImageX -t ^\"^%SystemDrive^%\Programs\GImageX\GImageX.exe\" -w \"^%SystemDrive^%\Programs\GImageX\" -icon \"%SystemDrive%\Programs\GImageX\GImageX.exe\" -a \"%*\"")
		print("")
		print("URL:")
		print(f"\t{fname} -n Links -t \"https://url\" -u")
		sys.exit(0)
	
	if not (args.ink != '' and args.ink != 'example' and args.target != ''):
		parser_dict['parser'].parse_args(['-h'])
		sys.exit(0)
	else:
		inpath = pathlib.Path(args.inpath).resolve()
		if not inpath.exists():
			inpath.mkdir(parents=True)
		ink = inpath.joinpath(args.name).resolve()
		if not ink.exists():
			if args.target != '':
				if args.url:
					link = win32com.client.Dispatch("WScript.Shell").CreateShortcut(f"{ink}.url")
				else:
					link = win32com.client.Dispatch("WScript.Shell").CreateShortcut(f"{ink}.lnk")
					link.WorkingDirectory = args.working
					link.Arguments = args.arguments
					link.IconLocation = args.icon
				link.TargetPath = args.target
				link.Save()
				sys.exit(0)

if __name__ == '__main__':
	main()
