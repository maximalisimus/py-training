#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pip install icmplib

from icmplib import ping
from icmplib.exceptions import NameLookupError, SocketPermissionError, SocketAddressError, ICMPSocketError

from os import environ
import pathlib

import sys

def GetPingList(onFile: str = '') -> tuple:
	#print('Loading a list of addresses for pings')
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

def FastOnePing(addr: str, count = 4, interval: float = 0.5, pocket_size: int = 64, timeout: float = 2, source: str = None):
	out_text = []
	try:
		host = ping(addr, count = count, interval = interval, payload_size = pocket_size, timeout = timeout, source = source)
	except NameLookupError:
		out_text.append(f"PING {addr} {pocket_size} bytes of data.\nReply from {addr}\nNot available...")
	except (SocketPermissionError, SocketAddressError, ICMPSocketError) as err:
		out_text.append(str(type(err).__name__))
	except:
		pass
	else:
		out_text.append(f"PING {addr} ({host.address}) {pocket_size} bytes of data.")
		rtts = map(lambda x: f"{x:.3f}", host.rtts)
		for item in rtts:
			out_text.append(f"{pocket_size} bytes from addr ({host.address}): time={item}")
		out_text.append(f"--- {addr} ping statistics ---")
		out_text.append(f"\t{host.packets_sent} packets transmitted, {host.packets_received} received, {int(host.packet_loss * 100)}% packet loss")
		out_text.append(f"rtt min/avg/max/jitter = {host.min_rtt}/{host.avg_rtt}/{host.max_rtt}/{host.jitter} ms")
	yield '\n'.join(out_text)

def main():
	file_hosts = str(environ.get('SYSTEMDRIVE')) + '\Windows\System32\drivers\etc\hosts'
	ping_list = GetPingList()
	full_ping = FastOnePing('ya.ru', timeout = 2)
	print(*full_ping)
	#oncount = 4
	#oninterval = 0.5
	#onsize = 64
	#full_ping = tuple(map(lambda x: FastOnePing(x, oncount, oninterval, onsize), ping_list))
	#for y in full_ping:
	#	for x in y:
	#		print(x)
	#	print()

if __name__ == '__main__':
	main()
