import sys
import pathlib
import configparser
import argparse
import json

from .default import SimpleJSON, FullJSON, default_template, dir_template, list_template
from .filespath import Files, Icon
from .operations import *

__author__ = 'Mikhail Artamonov'
__progname__ = str(pathlib.Path(sys.argv[0]).resolve().name)
__copyright__ = f"© The \"{__progname__}\". Copyright  by 2023."
__credits__ = ["Mikhail Artamonov"]
__license__ = "GPL3"
__version__ = "2.5.0"
__maintainer__ = "Mikhail Artamonov"
__email__ = "maximalis171091@yandex.ru"
__status__ = "Production"
__date__ = '28.08.2023'
__modifed__ = '28.08.2023'
__contact__ = 'VK: https://vk.com/shadow_imperator'

def main():
	pass

if __name__ == '__main__':
	main()
#else:
#	main()
