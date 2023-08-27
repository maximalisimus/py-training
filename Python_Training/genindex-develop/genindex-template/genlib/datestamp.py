__all__ = 'stampToStr stampToDateTime dateSTRToStamp dateTimeToStamp dateTimeToStr strToDateTime'.split()

from datetime import datetime
import time

def stampToStr(timeStamp: int, strFormat = "%d.%m.%Y-%H:%M:%S") -> str:
	dateTime = datetime.fromtimestamp(timeStamp)
	datestr = dateTime.strftime(strFormat)
	return datestr

def stampToDateTime(timeStamp: int) -> datetime:
	dateTime = datetime.fromtimestamp(timeStamp)
	return dateTime

def dateSTRToStamp(dateStr: str, strFormat = "%d.%m.%Y-%H:%M:%S") -> int:
	time_Tuple = datetime.strptime(dateStr, strFormat)
	outTimeStamp = time.mktime(time_Tuple.timetuple())
	return int(outTimeStamp)

def dateTimeToStamp(dateTime: datetime) -> int:
	outTimeStamp = time.mktime(dateTime.timetuple())
	return int(outTimeStamp)

def dateTimeToStr(dateTime: datetime, strFormat = "%d.%m.%Y-%H:%M:%S") -> str:
	outDateTime = dateTime.strftime(strFormat)
	return outDateTime

def strToDateTime(dateStr: str, strFormat = "%d.%m.%Y-%H:%M:%S") -> datetime:
	time_Tuple = datetime.strptime(dateStr, strFormat)
	return time_Tuple

