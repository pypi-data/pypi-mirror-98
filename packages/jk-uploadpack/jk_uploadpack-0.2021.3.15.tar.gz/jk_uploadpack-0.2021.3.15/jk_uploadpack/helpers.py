


import hashlib



#
# Consumer that iterates through a bytes iterator and produces the hash value.
#
def sha256_bytesiter(bytesiter) -> str:
	hasher = hashlib.sha256()
	for block in bytesiter:
		hasher.update(block)
	return hasher.hexdigest()
#



#
# Iterator that reads from a file.
#
def file_read_blockiter(f, blocksize=65536):
	block = f.read(blocksize)
	while len(block) > 0:
		yield block
		block = f.read(blocksize)
#





