__all__ = ['dir_template', 'default_file', 'default_template', 'list_template', 'size_format', 'SimpleJSON', 'FullJSON']

import sys
import pathlib

dir_template = str(pathlib.Path(sys.argv[0]).parent.joinpath('extension.template').resolve())
default_template = 'simplegen'

default_file = str(pathlib.Path(dir_template).joinpath(default_template).joinpath('file.png').resolve())
list_template = list(map(lambda y: str(y.name), filter(lambda x: x.is_dir(), sorted(pathlib.Path(dir_template).glob('*')))))

def size_format(in_size: int) -> str:
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

def SimpleJSON() -> dict:
	return {
			"standart": {
				"file_icon": "file",
				"folder_icon": "folder",
				"back_icon": "back"
			},
			"others": {
				"ar": "ar,zip,rar,gz,xz,gz2",
				"image": "jpg,png,gif,tiff,svg",
				"music": "mp3,wav,ogg,flac",
				"package": "deb,rpm",
				"patch": "patch",
				"pdf": "pdf",
				"script": "sh,py,rb,vbs,ps1",
				"document": "xls,odt,ods,doc,docx,xlsx",
				"conf": "conf,ini,asc"
			}
	}

def FullJSON() -> dict:
	return {
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
			"p0g0h": "veg",
			"6p3x3": "reg"
		}
	}
