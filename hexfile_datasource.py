"""
This plugin is an example for a custom Data Source.

It loads binary data from a hex encoded file.
"""

import binascii, os
import logging
from pre_workbench.bbuf_parsing import apply_grammar_on_bbuf
from pre_workbench.datasource import DataSourceTypes, SyncDataSource, formatinfoSelect
from pre_workbench.configs import SettingsField
from pre_workbench.objects import ByteBuffer

@DataSourceTypes.register(DisplayName="Hex file")
class FileDataSource(SyncDataSource):
	@staticmethod
	def getConfigFields():
		return [
			SettingsField("fileName", "File name", "text", {"fileselect": "open"}),
			SettingsField("formatInfo", "Grammar definition", "text", {"listselectcallback":formatinfoSelect})
		]
	def process(self):
		bbuf = ByteBuffer(metadata={'fileName': self.params['fileName'],
									'fileTimestamp': os.path.getmtime(self.params['fileName'])})
		with open(self.params['fileName'], "rb") as f:
			bbuf.setContent(binascii.unhexlify(f.read()))
		apply_grammar_on_bbuf(bbuf, self.params["formatInfo"])
		return bbuf
