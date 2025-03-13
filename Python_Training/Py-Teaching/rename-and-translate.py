#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib

class Translator:
	
	def __set_name__(self, owner, name):
		self.name = "__" + name
	
	def __get__(self, instance, owner):
		return {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'eo', 'ж': 'j', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 
				'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'x', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 
				'щ': 'sh', 'ъ': 'i', 'ы': 'iu', 'ь': 'i', 'э': 'e', 'ю': 'iu', 'я': 'ia'}

class Alphabet:
	
	lang = Translator()
	
	@classmethod
	def translate(cls, value: str) -> str:
		outline = ''
		for item in value:
			if item.lower() in cls.lang.keys():
				if item.islower():
					outline += cls.lang[item]
				else:
					outline += cls.lang[item.lower()].upper()
			else:
				outline += item
		return outline

def main():
	folder = pathlib.Path('./1C-8.2-Icons').resolve()
	on_files = folder.glob('*.png')
	for png_files in on_files:
		ext = str(png_files.name).split('.')[1]
		fname = str(png_files.name).split('.')[0]
		new_fname = Alphabet.translate(fname).replace(' ', '-')
		new_file = f"{new_fname}.{ext}"
		output_file = folder.joinpath(new_file)
		count = 0
		if output_file.exists():
			while output_file.exists():
				new_file = f"{new_fname}-{count}.{ext}"
				output_file = folder.joinpath(new_file)
				count += 1
			new_file = f"{output_file}"
		png_files.rename(new_file)
	pass

if __name__ == '__main__':
	main()
