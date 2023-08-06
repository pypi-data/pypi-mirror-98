


import os
import typing

import jk_utils





class UPFile(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self, fileGroup, directory, fileName:str, user:typing.Union[str,None], group:typing.Union[str,None], mode:typing.Union[int,str,None], fileID:int):
		assert fileGroup.__class__.__name__ == "UPFileGroup"
		self.__fileGroup = fileGroup

		assert directory.__class__.__name__ == "UPDir"
		self.__directory = directory

		assert isinstance(fileName, str)
		assert fileName
		assert "/" not in fileName
		assert "\\" not in fileName
		assert ":" not in fileName
		assert "|" not in fileName
		self.fileName = fileName

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

		assert isinstance(fileID, int)
		assert fileID >= 0
		self.__fileID = fileID
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def fileGroup(self):
		return self.__fileGroup
	#

	#
	# @return		UPDir		The directory this file resides in
	#
	@property
	def directory(self):
		return self.__directory
	#

	#
	# The file identifier. The content of this file is identified by this number.
	#
	@property
	def fileID(self) -> bool:
		return self.__fileID
	#

	@property
	def relFilePath(self) -> str:
		if self.__directory.relDirPath:
			return self.__directory.relDirPath + "/" + self.fileName
		else:
			return self.fileName
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def getEffectiveFileMode(self) -> typing.Union[int,None]:
		if self.mode is not None:
			return self.mode
		return self.__fileGroup.fileMode
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
			self.fileName,
			self.user,
			self.group,
			self.mode,
			self.__fileID,
		]
	#

	@staticmethod
	def fromJSON(fileGroup, directory, jData):
		assert isinstance(jData, (tuple,list))
		assert len(jData) == 5		# version 1 has 5 entries

		args = [ fileGroup, directory ] + jData

		return UPFile(*args)
	#

#







