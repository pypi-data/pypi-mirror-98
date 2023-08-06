


import stat
import os
import typing
import hashlib

import jk_typing

from .helpers import sha256_bytesiter, file_read_blockiter






#
# This class represents a source file to store. It provides essential information about that file for storing.
#
class SrcFileInfo(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self, size:int, hashID:str, srcFilePath:str, mode:int, mtime:float):
		assert isinstance(size, int)
		assert size >= 0
		assert isinstance(hashID, str)
		assert hashID
		assert isinstance(srcFilePath, str)
		assert srcFilePath
		assert isinstance(mode, int)
		assert isinstance(mtime, (int, float))

		self.mode = mode
		self.size = size
		self.mtime = mtime
		self.hashID = hashID
		self.srcFilePath = srcFilePath
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	@staticmethod
	def fromFile(filePath:str):
		statStruct = os.lstat(filePath)
		mode = statStruct.st_mode
		size = statStruct.st_size
		uid = statStruct.st_uid
		gid = statStruct.st_gid
		mtime = float(statStruct.st_mtime)

		hashAlg = hashlib.sha256()
		with open(filePath, "rb") as fin:
			for chunk in iter(lambda: fin.read(4096), b""):
				hashAlg.update(chunk)
		hashDigest = hashAlg.hexdigest()
		hashID = "sha256:{}:{}".format(hashDigest, size)

		return SrcFileInfo(size, hashID, filePath, mode, mtime)
	#

#







