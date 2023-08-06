


import os
import typing

import jk_utils



from .UPFile import UPFile




class UPDir(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self,
			fileGroup,
			relDirPath:str,
			user:typing.Union[str,None],
			group:typing.Union[str,None],
			mode:typing.Union[int,str,None],
			bCleanDir:typing.Union[bool,None],
			files:list,
		):
		assert fileGroup.__class__.__name__ == "UPFileGroup"
		self.__fileGroup = fileGroup

		assert isinstance(relDirPath, str)
		assert ":" not in relDirPath
		assert "|" not in relDirPath
		assert not relDirPath.endswith("/")
		self.relDirPath = relDirPath

		if user is not None:
			assert isinstance(user, str)
			assert user
		self.user = user

		if group is not None:
			assert isinstance(group, str)
			assert group
		self.group = group

		if mode is not None:
			if isinstance(mode, str):
				mode = jk_utils.ChModValue(mode).toInt()
			else:
				assert isinstance(mode, int)
		self.mode = mode

		if bCleanDir is not None:
			assert isinstance(bCleanDir, bool)
		self.bCleanDir = bCleanDir

		assert isinstance(files, list)
		for f in files:
			assert isinstance(f, UPFile)
		self.files = files
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def fileGroup(self):
		return self.__fileGroup
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def getEffectiveCleanDir(self) -> bool:
		if self.bCleanDir is not None:
			return self.bCleanDir
		if self.__fileGroup.bCleanDir is not None:
			return self.__fileGroup.bCleanDir
	#

	def getEffectiveFileMode(self) -> typing.Union[int,None]:
		if self.mode is not None:
			return self.mode
		return self.__fileGroup.dirMode
	#

	def getEffectiveUser(self) -> typing.Union[str,None]:
		if self.user is not None:
			return self.user
		return self.__fileGroup.user
	#

	def getEffectiveGroup(self) -> typing.Union[str,None]:
		if self.group is not None:
			return self.group
		return self.__fileGroup.group
	#

	def toJSON(self) -> list:
		return [
			self.relDirPath,
			self.user,
			self.group,
			self.mode,
			self.bCleanDir,
			[ f.toJSON() for f in self.files ],
		]
	#

	@staticmethod
	def fromJSON(fileGroup, jData):
		assert fileGroup

		assert isinstance(jData, (tuple,list))
		assert len(jData) == 6		# version 1 has 5 entries

		args = [ fileGroup ] + list(jData)
		args[-1] = []
		ret = UPDir(*args)

		for j in jData[-1]:
			ret.files.append(UPFile.fromJSON(fileGroup, ret, j))

		return ret
	#

#







