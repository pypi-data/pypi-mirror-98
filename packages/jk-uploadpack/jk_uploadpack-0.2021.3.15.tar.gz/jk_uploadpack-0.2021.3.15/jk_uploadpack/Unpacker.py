

import json
import tarfile
import os
import typing

from jk_terminal_essentials import Spinner

from .UPFile import UPFile
from .UPDir import UPDir
from .UPFileGroup import UPFileGroup
from .helpers import sha256_bytesiter, file_read_blockiter





class Unpacker(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self, archiveFilePath:str):
		assert isinstance(archiveFilePath, str)
		if archiveFilePath.endswith(".gz"):
			compression = "gz"
		elif archiveFilePath.endswith(".xz"):
			compression = "xz"
		elif archiveFilePath.endswith(".bz2"):
			compression = "bz2"
		else:
			compression = None
		self.__archiveFilePath = archiveFilePath

		# ----

		self.__fileGroups = {}
		self.__dirsCreated = set()
		self.__totalSizeUnpacked = 0
		self.__totalSizePacked = os.lstat(archiveFilePath).st_size

		# ----

		# open
		self.__t = tarfile.open(archiveFilePath, "r:{}".format(compression) if compression else "r")

		# store index (str -> TarInfo
		self.__tIndex = { ti.name:ti for ti in self.__t.getmembers() }

		# extract meta data
		data = self.__t.extractfile(self.__tIndex["meta.json"])
		jMeta = json.load(data)

		# verify meta data
		assert jMeta["magic"]["magic"] == "upload-pack"
		assert jMeta["magic"]["version"] == 1				# currently there is only a version 1

		# extract file groups
		jFileGroups = jMeta["fileGroups"]
		for fileGroupName, jFileGroupData in jFileGroups.items():
			fg = UPFileGroup.fromJSON(self, fileGroupName, jFileGroupData)
			self.__fileGroups[fg.identifier] = fg
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def fileGroupIdentifiers(self) -> list:
		return sorted(self.__fileGroups.keys())
	#

	@property
	def totalSizeCompressed(self) -> int:
		return self.__totalSizePacked
	#

	@property
	def totalSizePacked(self) -> int:
		return self.__totalSizePacked
	#

	@property
	def totalSizeLogical(self) -> int:
		return self.__totalSizeUnpacked
	#

	@property
	def totalSizeUnpacked(self) -> int:
		return self.__totalSizeUnpacked
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

	def _createDir(self, dirPath:str):
		if dirPath in self.__dirsCreated:
			return
		os.makedirs(dirPath, exist_ok=True)
		self.__dirsCreated.add(dirPath)
	#

	def _unpackToDir(self, file:UPFile, outBaseDirPath:str, sp:Spinner = None) -> typing.Tuple[str,str]:
		assert isinstance(file, UPFile)
		assert isinstance(outBaseDirPath, str)
		if sp is not None:
			assert isinstance(sp, Spinner)

		# ----

		_s = "parts/" + str(file.fileID)
		ti = self.__tIndex[_s]
		tf = self.__t.extractfile(_s)

		if sp:
			sp.spin("unpack", file.relFilePath)

		targetFilePath = os.path.join(outBaseDirPath, file.relFilePath)
		targetDirPath = os.path.dirname(targetFilePath)

		self._createDir(targetDirPath)

		tempFilePath = targetFilePath + ".$$$uploadpack$unpack$$$"
		with open(tempFilePath, "wb") as fout:
			for block in file_read_blockiter(tf):
				fout.write(block)
				self.__totalSizeUnpacked += len(block)

		if os.path.isfile(targetFilePath):
			os.unlink(targetFilePath)
		os.rename(tempFilePath, targetFilePath)

		return targetDirPath, os.path.basename(targetFilePath)
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def fileGroup(self, identifier:str) -> typing.Union[UPFileGroup,None]:
		assert isinstance(identifier, str)
		assert identifier

		return self.__fileGroups.get(identifier)
	#

	def close(self):
		if self.__t:
			self.__t.close()
			self.__t = None
	#

#









