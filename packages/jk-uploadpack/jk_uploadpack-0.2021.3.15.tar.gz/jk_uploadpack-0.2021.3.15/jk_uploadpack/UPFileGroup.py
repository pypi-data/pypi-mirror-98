


import os
import typing
import shutil

import jk_pathpatternmatcher2
from jk_terminal_essentials import Spinner

from .SrcFileInfo import SrcFileInfo
from .UPStoredBlob import UPStoredBlob
from .UPDir import UPDir
from .UPFile import UPFile





class UPFileGroup(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	# @param		UPDir[] dirs			(optional) A list of already existing UPDir objects.
	#
	def __init__(self, parent, identifier:str):
		self.__identifier = identifier
		self.__parent = parent

		self.__directories = {}
		self.__files = []

		self.user = None			# str
		self.group = None			# str
		self.fileMode = None		# int
		self.dirMode = None			# int
		self.bCleanDir = None		# bool
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def identifier(self) -> str:
		return self.__identifier
	#

	@property
	def files(self) -> typing.List[UPFile]:
		return self.__files
	#

	@property
	def directories(self) -> typing.List[UPDir]:
		sortedDirNames = sorted(self.__directories.keys())
		return [ self.__directories[dn] for dn in sortedDirNames ]
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __addExistingDir(self, d):
		self.__directories[d.relDirPath] = d
		self.__files.extend(d.files)
	#

	def __allParentDirs(self, fullPath:str, outBaseDirPath:str):
		while len(fullPath) > 1:
			baseDir = os.path.dirname(fullPath)
			yield baseDir
			if baseDir == outBaseDirPath:
				break
			fullPath = baseDir
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def toJSON(self) -> dict:
		sortedDirNames = sorted(self.__directories.keys())
		ret = {
			"user": self.user,
			"group": self.group,
			"fileMode": self.fileMode,
			"dirMode": self.dirMode,
			"bCleanDir": self.bCleanDir,
			"dirs": [ self.__directories[dn].toJSON() for dn in sortedDirNames ],
			#"files": [ f.toJSON() for f in self.__files ]
		}
		return ret
	#

	@staticmethod
	def fromJSON(parent, identifier:str, jData:dict):
		fileGroup = UPFileGroup(parent, identifier)

		fileGroup.user = jData["user"]
		fileGroup.group = jData["group"]
		fileGroup.fileMode = jData["fileMode"]
		fileGroup.dirMode = jData["dirMode"]
		fileGroup.bCleanDir = jData["bCleanDir"]

		for jDirData in jData["dirs"]:
			fileGroup.__addExistingDir(UPDir.fromJSON(fileGroup, jDirData))

		return fileGroup
	#

	def addFile(self, absFilePath:str, storageFilePath:str) -> UPFile:
		assert isinstance(absFilePath, str)

		assert isinstance(storageFilePath, str)
		assert storageFilePath
		assert storageFilePath[0] not in "/\\"
		storageFilePath = storageFilePath.replace("\\", "/")

		srcFI, sf = self.__parent._registerFile(absFilePath)
		assert isinstance(srcFI, SrcFileInfo)
		assert isinstance(sf, UPStoredBlob)

		relDirPath = os.path.dirname(storageFilePath)
		fileName = os.path.basename(storageFilePath)

		di = self.__directories.get(relDirPath)
		if di is None:
			di = UPDir(self, relDirPath, None, None, None, None, [])		# TODO: use user, use mode, use bClean?
			self.__directories[relDirPath] = di

		fi = UPFile(self, di, fileName, None, None, None, sf.fileID)
		di.files.append(fi)
		self.__files.append(fi)		# TODO: use user, use mode?
		return fi
	#

	def unpackToDir(self, outBaseDirPath:str, sp:Spinner = None):
		outBaseDirPath = os.path.abspath(outBaseDirPath)

		validDirectories = set()
		validDirectories.add(outBaseDirPath)
		validFiles = set()

		for f in self.__files:
			absTargetDirPath, fileName = self.__parent._unpackToDir(f, outBaseDirPath, sp)
			validDirectories.add(absTargetDirPath)
			for d in self.__allParentDirs(absTargetDirPath, outBaseDirPath):
				validDirectories.add(d)
			validFiles.add(os.path.join(absTargetDirPath, fileName))

		dirsToDelete = []
		filesToDelete = []

		for e in jk_pathpatternmatcher2.walk(
				outBaseDirPath,
				acceptDirPathPatterns="**/*",
				acceptFilePathPatterns="**/*",
				acceptLinkPathPatterns="**/*",
			):

			if e.typeID == "d":
				# dir
				if e.fullPath not in validDirectories:
					dirsToDelete.append(e)
			elif e.typeID == "e":
				# error
				raise Exception("ERROR: " + repr(e.exception))
			else:
				# file or link
				if e.fullPath not in validFiles:
					filesToDelete.append(e)

		for e in filesToDelete:
			updir = self.__directories.get(e.relDirPath)
			if updir and updir.getEffectiveCleanDir():
				if sp:
					sp.spin("delete", e.relFilePath, bPrintPercent=False)
				os.unlink(e.fullPath)

		for e in dirsToDelete:
			updir = self.__directories.get(e.relDirPath)
			if updir and updir.getEffectiveCleanDir():
				if sp:
					sp.spin("delete", e.relFilePath, bPrintPercent=False)
				shutil.rmtree(e.fullPath)
	#

#






