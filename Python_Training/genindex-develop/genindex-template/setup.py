from setuptools import setup, find_packages
from os.path import join, dirname

# python setup.py sdist bdist_wheel
# python setup.py install
# pip install .

setup(
    name='blacklist-scripts',
    version='2.4.3',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    author='Mikhail Artamonov',
    author_email='maximalis171091@yandex.ru',
    url='https://github.com/maximalisimus/blacklist-scripts.git',
    packages=find_packages(include=['pyblacklist', '*.py']),
    include_package_data=True,
    entry_points={
        'console_scripts': ['blacklist=pyblacklist.pyblacklist:main']
    },
    keywords = ["blacklist", "pyblacklist", "py-blacklist", 'blacklist-scripts'],
	classifiers = [
		"Programming Language :: Python",
		"Programming Language :: Python :: 3",
		"Development Status :: 3 public release",
		"License :: OSI Approved :: GNU GENERAL PUBLIC LICENSE Version 3 (GPL3)",
		"Operating System :: Linux",
		"Topic :: Utilities",
		],
	python_requires='>=3.0',
)
