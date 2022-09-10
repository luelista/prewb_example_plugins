import binascii
import hashlib

from pre_workbench.structinfo import ExprFunctions


@ExprFunctions.register()
def shex(i):
	if isinstance(i, (bytes, bytearray)):
		return binascii.hexlify(i).decode('ascii')
	else:
		return "%x" % i

def make_hashfun(hash_name):
	print("Registering hash function ",hash_name)
	def hash_(val):
		return hashlib.new(hash_name, val).digest()

	hash_.__name__ = hash_name
	ExprFunctions.register()(hash_)

for hash in hashlib.algorithms_available:
	make_hashfun(hash)
