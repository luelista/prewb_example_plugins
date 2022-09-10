import hashlib
from binascii import hexlify

from pre_workbench.configs import SettingsField
from pre_workbench.controls.hexview_selheur import SelectionHelpers, rangeBefore, findInRange
from PyQt5.QtGui import QColor, QPen, QPainter

def rangeAfter(bbuf, range, amount=16):
	(bufIdx, selMin, selMax) = range
	return bufIdx, selMax, min(bbuf.length, selMax + amount)

@SelectionHelpers.register(color="#ffff00", defaultEnabled=False, options=[
	SettingsField("hash_md5", "Match MD5", "check", {"default":False}),
	SettingsField("hash_sha1", "Match SHA1", "check", {"default":False}),
	SettingsField("hash_sha224", "Match SHA224", "check", {"default":False}),
	SettingsField("hash_sha256", "Match SHA256", "check", {"default":False}),
	SettingsField("hash_sha384", "Match SHA384", "check", {"default":False}),
	SettingsField("hash_sha512", "Match SHA512", "check", {"default":False}),
])
def highlightHashes(editor, qp, bbuf, sel, options):
	"""
	Searches for hashes of the selection (see options).

	This matcher is loaded from a plugin.
	"""

	(bufIdx, selstart, selend) = sel
	sellen = selend - selstart + 1
	selbytes = bbuf.getBytes(selstart, sellen)

	ranges = [rangeBefore(bbuf, sel, 32), rangeAfter(bbuf, sel, 32)]
	searchFor = []
	for k,v in options.items():
		if not k.startswith("hash_"): continue
		hash_name = k[5:]
		digest = hashlib.new(hash_name, selbytes).digest()
		hex_digest = hexlify(digest)
		searchFor.append((digest, hash_name))
		searchFor.append((hex_digest, hash_name))
		searchFor.append((hex_digest.upper(), hash_name))

	for match, desc in findInRange(bbuf, ranges, searchFor):
		editor.highlightMatch(qp, match, "Hash " + desc, QColor("#ffff00"))


