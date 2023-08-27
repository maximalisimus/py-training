__all__ = ['pack', 'unpack']

import tarfile
import pathlib

def pack(output_filename, source_dir):
	with tarfile.open(pathlib.Path(str(output_filename)).resolve(), "w:gz") as tar:
		#import os.path
		#tar.add(source_dir, arcname=os.path.basename(str(source_dir)))
		tar.add(source_dir, arcname=pathlib.Path(str(source_dir)).resolve().name)

def unpack(tarfiles, extract):
	path_tar = pathlib.Path(str(tarfiles)).resolve()
	if str(path_tar).endswith("tar.gz"):
		with tarfile.open(path_tar, 'r:gz') as tar_file:
			tar_file.extractall(pathlib.Path(str(extract)).resolve())
	elif str(path_tar).endswith("tar"):
		with tarfile.open(path_tar, 'r:') as tar_file:
			tar_file.extractall(pathlib.Path(str(extract)).resolve())
