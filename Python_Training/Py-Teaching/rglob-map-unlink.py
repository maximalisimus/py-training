#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib

def main():
	p = sorted(pathlib.Path('./pkg').rglob('*.py'))
	list(map(lambda x: x.unlink(missing_ok = True), p))

if __name__ == '__main__':
	main()
