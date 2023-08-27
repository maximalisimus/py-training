__all__ = ['SearchDictValue', 'RandName']

def SearchDictValue(OnDict: dict, onKey: str):
	def CheckSTR(in_str: str, OnKey: str) -> bool:
		for x in in_str.split(','):
			if OnKey.lower() == x.lower():
				return True
		return False
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
