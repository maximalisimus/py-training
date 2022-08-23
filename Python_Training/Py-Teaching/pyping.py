#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pip install icmplib

from icmplib import ping, multiping
from icmplib.exceptions import NameLookupError, SocketPermissionError, SocketAddressError, ICMPSocketError

def FastOnePing(addr: str, counter = 3, interval: float = 0.2, pocket_size: int = 64):
	try:
		host = ping(addr, count = counter, interval = interval, payload_size = pocket_size)
	except NameLookupError:
		print(f"PING {addr} {pocket_size} bytes of data.")
		print(f"Reply from {addr}")
		print(f"Not available...")
	except (SocketPermissionError, SocketAddressError, ICMPSocketError) as err:
		print(type(err).__name__, err.message)
	else:
		print(f"PING {addr} ({host.address}) {pocket_size} bytes of data.")
		rtts = map(lambda x: f"{x:.3f}", host.rtts)
		for item in rtts:
			print(f"{pocket_size} bytes from addr ({host.address}): time={item}")
		print(f"--- {addr} ping statistics ---")
		print(f"{host.packets_sent} packets transmitted, {host.packets_received} received, {int(host.packet_loss * 100)}% packet loss")
		print(f"rtt min/avg/max/jitter = {host.min_rtt}/{host.avg_rtt}/{host.max_rtt}/{host.jitter} ms")

def FastMultiPing(addr: tuple, counter = 3, interval: float = 0.5, pocket_size: int = 64):
	try:
		hosts = multiping(addr, count = counter, interval = interval, payload_size = pocket_size)
	except NameLookupError:
		pass
	except (SocketPermissionError, SocketAddressError, ICMPSocketError) as err:
		pass
	else:
		for key in range(len(addr)):
			print(f"PING {addr[key]} ({hosts[key].address}) {pocket_size} bytes of data.")
			rtts = map(lambda x: f"{x:.3f}", hosts[key].rtts)
			for item in rtts:
				print(f"{pocket_size} bytes from addr ({hosts[key].address}): time={item}")
			print(f"--- {addr[key]} ping statistics ---")
			print(f"{hosts[key].packets_sent} packets transmitted, {hosts[key].packets_received} received, {int(hosts[key].packet_loss * 100)}% packet loss")
			print(f"rtt min/avg/max/jitter = {hosts[key].min_rtt}/{hosts[key].avg_rtt}/{hosts[key].max_rtt}/{hosts[key].jitter} ms")

def main():
	address = 'no-ping.lost.com'
	FastOnePing(address)
	address = ('ya.ru', '8.8.8.8', '127.0.0.1')
	FastMultiPing(address)
	pass

if __name__ == '__main__':
	main()
