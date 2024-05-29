#!/usr/bin/env python3
# -*- coding: utf-8 -*-

LF = '\n'
CRLF = '\r\n'
CR = '\r'


def _normalize_line_endings(lines, line_ending='unix'):
	r"""Normalize line endings to unix (\n), windows (\r\n) or mac (\r).

	:param lines: The lines to normalize.
	:param line_ending: The line ending format.
	Acceptable values are 'unix' (default), 'windows' and 'mac'.
	:return: Line endings normalized.
	"""
	lines = lines.replace(CRLF, LF).replace(CR, LF)
	if line_ending == 'windows':
		lines = lines.replace(LF, CRLF)
	elif line_ending == 'mac':
		lines = lines.replace(LF, CR)
	return lines
