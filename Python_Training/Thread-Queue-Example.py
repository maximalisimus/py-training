#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://yandex.ru/search/?clid=1882628&text=python+thread&l10n=ru&lr=37146
# python thread

import Queue
import threading
import urllib2

# Called by each thread
def get_url(q, url):
	q.put(urllib2.urlopen(url).read())
	
theurls = ["http://google.com", "http://yahoo.com"]

q = Queue.Queue()
for u in theurls:
	t = threading.Thread(target=get_url, args = (q,u))
	t.daemon = True
	t.start()
s = q.get()
print s





