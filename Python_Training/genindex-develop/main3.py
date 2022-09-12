#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pathlib
import configparser
import argparse

__version__ = '1.0.0'
progname = 'genindex'

PREFIX = pathlib.Path(sys.argv[0]).resolve().parent

config_file = PREFIX.joinpath('config.ini')

class Arguments:
	
	def __getattr__(self, attrname):
		return None
	
	def __repr__(self):
		return f"{self.__class__}:  (\n" + \
				f"\tFonts: {self.fonts},\n" + \
				f"\tBGColor: {self.bgcolor},\n" + \
				f"\tEvenOdd: {self.evenodd},\n" + \
				f"\tOddEven: {self.oddeven},\n" + \
				f"\tSkip Dirs: {self.skip_dirs},\n" + \
				f"\tSkip Files: {self.skip_files},\n" + \
				f"\tSave configs: {self.save},\n" + \
				f"\tReset configs: {self.reset},\n" + \
				f"\tDirs: {self.dirs},\n" + \
				f"\tGenerate Icon Flag: {self.generate},\n" + \
				f"\tWrite Html Flag: {self.write}"

def createParser():
	parser = argparse.ArgumentParser(prog=progname,description='GenIndex - create apindex file.')
	group1 = parser.add_argument_group('Default', 'Default paramters.')
	parser.add_argument('-v', '--version', action='version', version=f'{progname} {__version__}',  help='Version.')
	group1.add_argument("-f", '--fonts', dest="fonts", metavar='FONTS', type=str, default='sans-serif', help='Html page font.')
	group1.add_argument("-b", '--bgcolor', dest="bgcolor", metavar='BGCOLOR', type=str, default='white', help='Background color Html page.')
	group1.add_argument("-e", '--evenodd', dest="evenodd", metavar='EVENODD', type=str, default='white', help='Color of odd lines of Html page.')
	group1.add_argument("-o", '--oddeven', dest="oddeven", metavar='ODDEVEN', type=str, default='#C9E4F6', help='Color of even lines of the Html page.')
	
	group2 = parser.add_argument_group('Skip', 'SKIP paramters.')
	group2.add_argument("-sd", '--skip_dirs', dest="skip_dirs", metavar='SKIP_DRIS', type=str, default='git,.git', help='Skip Directories.')
	group2.add_argument("-sf", '--skip_files', dest="skip_files", metavar='SKIP_FILES', type=str, default='', help='Skip Files.')
	
	group3 = parser.add_argument_group('Save', 'Save paramters.')
	group3.add_argument('-s', '--save', action='store_true', default=False, help='Save configs.')
	group3.add_argument('-r', '--reset', action='store_true', default=False, help='Reset settings to Default config.')
	
	group4 = parser.add_argument_group('Actions', 'Action paramters.')
	group4.add_argument("-d", '--dirs', dest="dirs", metavar='DIRS', type=str, default='./', help='Select the folder.')
	group4.add_argument('-g', '--generate', action='store_true', default=False, help='Generate Generate new name for icon file.')
	group4.add_argument('-w', '--write', action='store_true', default=False, help='Perform recording index.html files to the specified directory.')
	return parser, group1, group2, group3, group4

def DefaultConfig() -> dict:
	return {
			"fonts": 'sans-serif',
			"bgcolor": 'white',
			"evenodd": 'white',
			"oddeven": '#C9E4F6'
			}

def SkipConfig() -> dict:
	return {
			"dirs": 'git,.git',
			"files": ''
			}

def WriteDefaultConfig(parser):
	global config_file
	parser['HTML'] = DefaultConfig()
	parser['SKIP'] = SkipConfig()
	with open(config_file, 'w') as configfile:
		parser.write(configfile)

def WriteConfig(parser):
	global config_file
	with open(config_file, 'w') as configfile:
		parser.write(configfile)

def main():
	global config_file
	config = configparser.ConfigParser()
	if config.sections() == []:
		config.read(config_file)
	parser, gr1, gr2, gr3, gr4 = createParser()
	args = Arguments()
	parser.parse_args(namespace=Arguments)
	config['HTML']['fonts'] = args.fonts
	config['HTML']['bgcolor'] = args.bgcolor
	config['HTML']['evenodd'] = args.evenodd
	config['HTML']['oddeven'] = args.oddeven
	config['SKIP']['dirs'] = args.skip_dirs
	config['SKIP']['files'] = args.skip_files
	if args.save:
		WriteConfig(config)
	if args.reset:
		WriteDefaultConfig(config)
	# print(dict(config.items('HTML')))
	# print(dict(config.items('SKIP')))
	pass

if __name__ == '__main__':
	main()
