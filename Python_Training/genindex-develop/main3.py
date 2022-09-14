#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pathlib
import configparser
import argparse
import random
import json

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
				f"\tReset Icons: {self.reseticons}\n" + \
				f"\tDirs: {self.dirs},\n" + \
				f"\tGenerate Icon Flag: {self.generate},\n" + \
				f"\tInput icons: {self.inputicon},\n" + \
				f"\tList extensions: {self.ext},\n" + \
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
	group3.add_argument('-ri', '--reseticons', action='store_true', default=False, help='Reset icons settings to Default config.')
	
	group4 = parser.add_argument_group('Actions', 'Action paramters.')
	group4.add_argument("-d", '--dirs', dest="dirs", metavar='DIRS', type=str, default='./', help='Select the folder.')
	group4.add_argument('-g', '--generate', action='store_true', default=False, help='Generate Generate new name for icon file.')
	group4.add_argument('-i', '--inputicon', action='store_true', default=False, help='Icon input file.')
	group4.add_argument("-ext", '--ext', dest="ext", metavar='EXT', type=str, default='', help='Comma-separated list of extensions without spaces.')
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

def ConfigOnConfig(parser, arguments: Arguments):
	parser['HTML']['fonts'] = arguments.fonts
	parser['HTML']['bgcolor'] = arguments.bgcolor
	parser['HTML']['evenodd'] = arguments.evenodd
	parser['HTML']['oddeven'] = arguments.oddeven
	parser['SKIP']['dirs'] = arguments.skip_dirs
	parser['SKIP']['files'] = arguments.skip_files

def WriteIcons(data_icons: dict, file_icons: str = "template/icons.json"):
	global PREFIX
	with open(pathlib.Path(PREFIX).joinpath(file_icons).resolve(), "r", "w") as fp:
		json.dump(data_icons, fp, indent=2)

def WriteBasicIcons(file_icons: str = "template/icons.json"):
	global PREFIX
	data = {
			"standart": {
				"file_icon": "file",
				"folder_icon": "folder",
				"back_icon": "back"
			},
			"others": {
				"b5i9v": "arj,xz,cab,001,cpio,wim,swm,esd,fat,ntfs,dmg,hfs,xar,squashfs,apfs",
				"o2u3c": "tar",
				"e4z2n": "bz2,bzip,bz,bzip2,tbz2,tbz",
				"q7p4o": "rar",
				"6z3e8": "7z",
				"s1v5p": "zip,z",
				"i7h2r": "gz,gz2,tgz,tpz,txz,taz",
				"2p2l6": "lzma,lzh,lha",
				"b5j7k": "iso,mds,mdf,ccd,img,sub,cue,nrg,bwt,bwi,bws,cdi",
				"b7m2o": "bmp,jpeg,jpg,png,gif,tiff,svg,webdm,ico,cdr,eps,tex",
				"9y1g9": "xcf,gpl",
				"z1u3f": "psd,pdd,atn,abr,asl",
				"7l6i7": "dxf",
				"4u5x3": "FBX",
				"3x7d5": "max",
				"r3c4d": "SKP",
				"w6i3n": "eps",
				"a3g4e": "emf",
				"3d8n2": "wmf",
				"r1z6h": "kra",
				"c3t4s": "hlp",
				"d5g1v": "chm",
				"d5r4o": "mp3,wav,ogg,flac",
				"d7f2o": "mp4,avi,3gp,wmv,webm,mpeg,divx,mkv,m4v",
				"4l0c4": "aup",
				"w1t3b": "flv",
				"f4t3t": "deb",
				"f9j6j": "rpm",
				"g5f7m": "patch",
				"g9j9d": "pdf",
				"h2y4h": "doc,docx",
				"1c3f2": "odt",
				"i8k2z": "xls,xlsx",
				"2a7h0": "ods",
				"l3n4g": "ppt,pptx",
				"4a3u1": "odp",
				"j9p5i": "sql,db,dbf,dbc",
				"3b8e7": "acdb,acdc,adb,adf,alf,dxl,kdb,mdb",
				"3r6f2": "odb",
				"4d1f2": "kbx,kdbx",
				"5h1l2": "odg,otg,fodg",
				"3c4l2": "odf,mml",
				"l9k2n": "c",
				"m7t2p": "cpp",
				"n9o2x": "h",
				"p6l3m": "ino",
				"o6i7b": "log",
				"o8j5k": "html,htm,hta",
				"p4f4q": "css",
				"p7g3b": "php",
				"q4u5x": "pro",
				"r7s4y": "ttf,otf,fon,pfa,pfb,pfr,fnt",
				"r9b7l": "svg",
				"s3b4b": "sh,py,rb,vbs,ps1,AppImage,pl",
				"b5o2e": "java,class",
				"t2h1s": "bat,cmd",
				"w1l5d": "rtf,dot,csv,xml,txt,md,locale,mo,trans",
				"w4c1d": "conf,ini,asc,cnf,cur,ani,sys,mui,spl,inf",
				"x1q8u": "exe,msi,scr,run,bin",
				"n7p9z": "ovpn,vpn",
				"o1q5j": "gpg",
				"t5d0x": "sig,asc,sam,key,req",
				"p5x6t": "apk,tgz,zst",
				"k9r9s": "hdd",
				"e1c1h": "ova",
				"9o8i1": "ovf",
				"9q1t2": "vdi",
				"r9d3m": "vhd,vhdx",
				"8l5k7": "vmdk",
				"8o6y8": "qcow",
				"t0l5m": "desktop",
				"p7m9c": "info,nfo",
				"g7z2i": "dll,so,0,1,2",
				"n2b2e": "xml,msc,ps",
				"h7o6j": "json",
				"k0e1m": "lic,license",
				"y8w8p": "man",
				"c4i7v": "py",
				"h5e6d": "lib,dcm",
				"q6f3z": "bck,sum,sums,md5,sha,sha1,sha1sums,sha256sums,sha512sums,hash",
				"t0k2y": "kicad_mod,mod",
				"9g7i5": "kicad_sch,sch",
				"2f7y2": "kicad_pcb,pcb",
				"i9h7p": "lgr,pho,GTL,GBL,GBS,GTS,GBO,GTO,GBP,GTP,GKO,GPT,GPB,GM1,GM2,GM3,GM4,GM5,GM6,GM7,GM8,GM9",
				"x2i7d": "user",
				"z0w2a": "stl,wrl,dae,vrm,vrml",
				"k1w4m": "fcstd",
				"l5g6m": "blend,blende1,blende2,blend3,blend4,blend5",
				"8w4v9": "glade",
				"p0g0h": "veg"
			}
	}
	with open(pathlib.Path(PREFIX).joinpath(file_icons).resolve(), "r", "w") as fp:
		json.dump(data, fp, indent=2)

def ReadIcons(file_icons: str = "template/icons.json") -> dict:
	global PREFIX
	data = ''
	with open(pathlib.Path(PREFIX).joinpath(file_icons).resolve(), "r") as fp:
		data = json.load(fp)
	return data

def CheckSTR(in_str: str, OnKey: str) -> bool:
	for x in in_str.split(','):
		if OnKey.lower() == x.lower():
			return True
	return False

def SearchDictValue(OnDict: dict, onKey: str):
	for key, value in OnDict.items():
		if CheckSTR(value, onKey):
			return key
	return None

def RandName(OnDict: dict):
	alphabet1 = ''.join([chr(x).lower() for x in range(65,91)])
	sel = (True, False)
	output = ''
	def isDictKey(OnDict: dict, onKey: str):
		for key in OnDict.keys():
			if onKey == key:
				return True
		return False
	def GenName():
		rez = ''
		if random.choice(sel):
			rez = random.choice(alphabet1) + \
					str(random.randint(0, 9)) + \
					random.choice(alphabet1) + \
					str(random.randint(0, 9)) + \
					random.choice(alphabet1)
		else:
			rez = str(random.randint(0, 9)) + \
					random.choice(alphabet1) + \
					str(random.randint(0, 9)) + \
					random.choice(alphabet1) + \
					str(random.randint(0, 9))
		return rez
	output = GenName()
	while isDictKey(OnDict, output):
		output = GenName()
	return output

def ReadConfig() -> Arguments:
	global config_file
	config = configparser.ConfigParser()
	if config.sections() == []:
		config.read(config_file)
	parser, gr1, gr2, gr3, gr4 = createParser()
	args = Arguments()
	parser.parse_args(namespace=Arguments)
	ConfigOnConfig(config, args)
	if args.save:
		WriteConfig(config)
		sys.exit(0)
	if args.reset:
		WriteDefaultConfig(config)
		sys.exit(0)
	if args.reseticons:
		WriteBasicIcons()
		sys.exit(0)
	if args.generate:
		data = ReadIcons()
		on_name = RandName(data['others'])
		print(on_name)
		sys.exit(0)
	return args

def main():
	on_args = ReadConfig()
	# print(on_args)
	#data = ReadIcons()
	#pattern = 'zip'
	#a = SearchDictValue(data['others'], pattern)
	#print(a)
	pass

if __name__ == '__main__':
	main()
