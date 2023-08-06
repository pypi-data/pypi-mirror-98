



import time
import os
import typing
import sys
import json
import tarfile
import io

import jk_utils

from .SrcFileInfo import SrcFileInfo
from .UPFile import UPFile
from .UPFileGroup import UPFileGroup
from .UPStoredBlob import UPStoredBlob






class Packer(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self, outFilePath:str, compression:str = None):
		assert isinstance(outFilePath, str)
		assert outFilePath
		self.__outFilePath = outFilePath

		# ----

		if compression is None:
			if outFilePath.endswith(".gz"):
				self.__compression = "gz"
			elif outFilePath.endswith(".xz"):
				self.__compression = "xz"
			elif outFilePath.endswith(".bz2"):
				self.__compression = "bz2"
			else:
				self.__compression = None
		else:
			assert isinstance(compression, str)
			assert compression in [ "gz", "gzip", "xz", "bz2", "bzip2" ]
			if compression == "bzip2":
				compression = "bz2"
			if compression == "gzip":
				compression = "gz"
			self.__compression = compression

		# ----

		self.__totalSizeLogical = 0
		self.__totalSizeUncompressed = 0
		self.__totalSizeCompressed = 0

		self.__fileGroups = {}

		self.__filesByID = []
		self.__filesByHash = {}

		self.__t = tarfile.open(outFilePath, ("w:" + self.__compression) if self.__compression else "w")
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def closed(self) -> bool:
		return self.__t is None
	#

	@property
	def isClosed(self) -> bool:
		return self.__t is None
	#

	@property
	def totalSizeLogical(self) -> int:
		return self.__totalSizeLogical
	#

	@property
	def totalSizeUncompressed(self) -> int:
		return self.__totalSizeUncompressed
	#

	@property
	def totalSizeCompressed(self) -> int:
		return self.__totalSizeCompressed
	#

	@property
	def fileGroupIdentifiers(self) -> list:
		return sorted(self.__fileGroups.keys())
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __enter__(self):
		return self
	#

	def __exit__(self, _extype, _exobj, _stacktrace):
		self.close()
	#

	def _registerFile(self, filePath:str) -> typing.Tuple[SrcFileInfo,UPStoredBlob]:
		srcFI = SrcFileInfo.fromFile(filePath)

		sf = self.__filesByHash.get(srcFI.hashID)
		if sf is None:
			fileID = len(self.__filesByID)

			tarInfo = tarfile.TarInfo("parts/{}".format(fileID))
			tarInfo.size = srcFI.size
			tarInfo.mtime = srcFI.mtime		# TODO
			tarInfo.uid = 1000				# TODO
			tarInfo.gid = 1000				# TODO
			tarInfo.mode = srcFI.mode		# TODO
			with open(srcFI.srcFilePath, "rb") as fin:
				self.__t.addfile(tarInfo, fin)
			sf = UPStoredBlob(fileID, srcFI.size)

			self.__filesByID.append(sf)
			self.__filesByHash[srcFI.hashID] = sf

			self.__totalSizeUncompressed += srcFI.size

		self.__totalSizeLogical += srcFI.size

		return srcFI, sf
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def fileGroup(self, identifier:str) -> UPFileGroup:
		assert isinstance(identifier, str)
		assert identifier

		fg = self.__fileGroups.get(identifier)
		if fg is None:
			fg = UPFileGroup(self, identifier)
			self.__fileGroups[identifier] = fg
		return fg
	#

	def __createMetaJSON(self) -> dict:
		_jFileGroups = {}
		for upFG in self.__fileGroups.values():
			_jFileGroups[upFG.identifier] = upFG.toJSON()

		return {
			"magic": {
				"magic": "upload-pack",
				"version": 1,
			},
			"fileGroups": _jFileGroups,
		}
	#

	def close(self):
		if self.__t is None:
			return

		rawData = json.dumps(self.__createMetaJSON()).encode("utf-8")

		tarInfo = tarfile.TarInfo("meta.json")
		tarInfo.size = len(rawData)
		tarInfo.mtime = time.time()
		tarInfo.uid = os.getuid()
		tarInfo.gid = os.getgid()
		tarInfo.mode = jk_utils.ChModValue("rwxrwxr-x").toInt()

		self.__totalSizeUncompressed += tarInfo.size

		self.__t.addfile(tarInfo, io.BytesIO(rawData))
		self.__t.close()
		self.__t = None

		self.__totalSizeCompressed = os.lstat(self.__outFilePath).st_size
	#

#













