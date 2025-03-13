#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib
import sys
import hashlib
import base64

class Characters:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return '.-+_,()[]{}&@#='

class AlphabetRU:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return ''.join(list(map(chr, range(ord('а'),ord('я')+1, 1))))

class AlphabetEN:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return ''.join(list(map(chr, range(ord('a'),ord('z')+1, 1))))

class Integers:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return ''.join(list(map(str, list(range(0, 10, 1)))))

class Alphabet:
	
	symbols = Characters()
	alphabet_ru = AlphabetRU()
	alphabet_en = AlphabetEN()
	nums = Integers()

	@property
	def alphabet(self):
		return self.alphabet_ru + self.alphabet_ru.upper() + ' ' + self.alphabet_en + self.alphabet_en.upper() + self.symbols + self.nums

	def SetName(self, onname):
		return ''.join([x for x in onname if x in self.alphabet]).replace(' ', '_')

class Texts:
	
	@classmethod
	def SetCorrectFileName(cls, inputFileName):
		alphabet = Alphabet()
		return alphabet.SetName(inputFileName)

class Meta(type):
	
	def __init__(cls, *args, **kwargs):
		super().__init__(*args, **kwargs)
	
	@property
	def PREFIX(cls):
		return pathlib.Path(sys.argv[0]).resolve().parent
	
	@property
	def access_file(cls):
		return f".htaccess"
	
	@property
	def pass_file(cls):
		return f".htpasswd"
	
class Files(metaclass=Meta):
	
	@staticmethod
	def read_write_file(onfile, typerw, data = ""):
		''' The function of reading and writing text files. '''
		file_save = pathlib.Path(str(onfile)).resolve()
		file_name = Texts.SetCorrectFileName(str(file_save.name))
		file_save = pathlib.Path(str(onfile)).resolve().parent.joinpath(file_name)
		file_save.parent.mkdir(parents=True,exist_ok=True)
		with open(str(file_save), typerw) as fp:
			if 'r' in typerw:
				data = fp.read()
				return data
			else:
				fp.write(data)

def htpasswd(username, password):
	hs= hashlib.sha1()
	hs.update(password.encode("utf-8"))
	login_word = username + ":{SHA}" + str(base64.b64encode(hs.digest()).decode("utf-8"))
	return login_word.strip()

def main():
	text_part_1 = f"AuthType Basic\nAuthName \"Private zone. Only for authorized!\"\nAuthUserFile"
	text_part_2 = f"./.htpasswd"
	text_part_3 = f"\nrequire valid-user"
	full_access_text = f"{text_part_1}{text_part_2}{text_part_3}"
	log_pass = htpasswd('admin', 'gfhjkm')
	Files.read_write_file(Files.PREFIX.joinpath(Files.access_file), 'w', full_access_text)
	Files.read_write_file(Files.PREFIX.joinpath(Files.pass_file), 'a', log_pass)
	pass

if __name__ == '__main__':
	main()
