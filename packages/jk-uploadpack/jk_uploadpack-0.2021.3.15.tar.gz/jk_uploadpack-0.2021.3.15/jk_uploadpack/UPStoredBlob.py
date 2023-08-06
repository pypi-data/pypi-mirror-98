


import os
import typing








#
# This class holds information about a file stored in the archive.
#
class UPStoredBlob(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self, fileID:int, size:int):
		assert isinstance(fileID, int)
		self.fileID = fileID

		assert isinstance(size, int)
		self.size = size
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

	def toJSON(self) -> list:
		assert isinstance(self.fileID, int)
		assert self.fileID >= 0

		assert isinstance(self.size, int)
		assert self.size >= 0

		return [
			1,
			self.fileID,
			self.size,
		]
	#

	@staticmethod
	def fromJSON(jData):
		assert isinstance(jData, (tuple,list))
		assert jData
		assert jData[0] == 1		# version
		assert len(jData) == 3		# version 1 has 3 entries

		return UPStoredBlob(
			fileID=jData[1],
			size=jData[2],
		)
	#

#







