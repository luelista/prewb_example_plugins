"""
This plugin is an example for a custom Data Source.

It shows a text editor which automatically stores its contents in the project database.
"""

import os

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox
from pre_workbench.guihelper import APP
from pre_workbench.rangetree import RangeTreeWidget
from pre_workbench.structinfo.parsecontext import AnnotatingParseContext
from pre_workbench.typeregistry import DockWidgetTypes
from pre_workbench.util import PerfTimer


@DockWidgetTypes.register(title="Selection Parser", icon="document-text.png", showFirstRun=True)
class SelectionParserWidget(QWidget):
	def __init__(self):
		super().__init__()
		self.selbytes = None
		self._initUI()
		self.loadFormatInfo()
		self.fiTreeWidget.formatInfoContainer.updated.connect(self.parse)

	def saveState(self):
		return {"hs": self.fiTreeWidget.header().saveState()}
	def restoreState(self, data):
		if "hs" in data: self.fiTreeWidget.header().restoreState(data["hs"])

	def on_selected_bytes_updated(self, selbytes):#buffer:ByteBuffer, range:Range):
		if not self.isVisible(): return
		self.selbytes = selbytes
		self.parse()

	def parse(self):
		with PerfTimer("DataInspector parsing"):
			if not self.selbytes: return
			parse_context = AnnotatingParseContext(self.fiTreeWidget.formatInfoContainer, self.selbytes) #buffer.getBytes(range.start, range.length()))
			fi_tree = parse_context.parse(by_name=self.definitionSelect.currentText())
			self.fiTreeWidget.updateTree([fi_tree])

	def _initUI(self):
		self.sourceSelect = QComboBox()
		self.sourceSelect.setEditable(True)
		self.sourceSelect.currentTextChanged.connect(self.loadFormatInfo)
		self.definitionSelect = QComboBox()
		self.definitionSelect.setEditable(True)
		self.definitionSelect.currentTextChanged.connect(self.parse)
		self.fiTreeWidget = RangeTreeWidget()
		windowLayout = QVBoxLayout()
		windowLayout.addWidget(self.sourceSelect)
		windowLayout.addWidget(self.definitionSelect)
		windowLayout.addWidget(self.fiTreeWidget)
		windowLayout.setContentsMargins(0,0,0,0)
		self.setLayout(windowLayout)

	def loadFormatInfo(self):
		filespec = self.sourceSelect.currentText()
		if filespec == "":
			self.fiTreeWidget.formatInfoContainer = APP().project.formatInfoContainer
		elif os.path.isfile(filespec):
			self.fiTreeWidget.loadFormatInfo(load_from_file=filespec)
		self.definitionSelect.clear()
		try:
			self.definitionSelect.addItems(self.fiTreeWidget.formatInfoContainer.definitions.keys())
		except:
			pass

