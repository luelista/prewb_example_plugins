"""
This plugin is an example for a custom Data Source.

It shows a text editor which automatically stores its contents in the project database.
"""
from PyQt5 import QtCore
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QToolBar, QShortcut, QAction, QTreeWidget, QTreeWidgetItem, \
	QAbstractItemView
from pre_workbench.algo.range import Range
from pre_workbench.configs import getIcon
from pre_workbench.typeregistry import DockWidgetTypes


@DockWidgetTypes.register(title="Histogram View", icon="chart.png", dock="Right", showFirstRun=False)
class HistogramViewWidget(QWidget):
	def __init__(self):
		super().__init__()
		self._initUI()
		self.hexview = None

	def _initUI(self):
		toolbar = QToolBar()
		self.cmdLineEdit = QComboBox(editable=True, minimumWidth=200)
		self.cmdLineEdit.setEditText("0x100")
		QShortcut(QKeySequence(QtCore.Qt.Key_Return), self.cmdLineEdit, activated=self._runTool, context=QtCore.Qt.WidgetWithChildrenShortcut)
		self._updateMru()
		toolbar.addWidget(self.cmdLineEdit)
		toolbar.addAction(getIcon("magnifier-left.png"), "Find", self._runTool)
		#self.displayAsHexAction = QAction(getIcon("document-binary.png"), "Display Results as Hex String", self, triggered=self._runTool)
		#self.displayAsHexAction.setCheckable(True)
		#toolbar.addAction(self.displayAsHexAction)

		self.treeView = QTreeWidget()
		self.treeView.setColumnCount(3)
		self.treeView.setColumnWidth(0, 200)
		self.treeView.setColumnWidth(1, 50)
		self.treeView.setColumnWidth(2, 100)
		self.treeView.headerItem().setText(0, "Range")
		self.treeView.headerItem().setText(1, "Entropy")
		self.treeView.headerItem().setText(2, "Entropy Graph")
		self.treeView.currentItemChanged.connect(self._currentItemChanged)
		self.treeView.setSelectionMode(QAbstractItemView.ExtendedSelection)
		windowLayout = QVBoxLayout()
		windowLayout.addWidget(toolbar)
		windowLayout.addWidget(self.treeView)
		windowLayout.setContentsMargins(0,0,0,0)
		self.setLayout(windowLayout)

	def _updateMru(self):
		self.cmdLineEdit.clear()

	def on_meta_updated(self, event_id, sender):
		if event_id != "hexview_range" or sender is None: return
		self.hexview = sender

	def _runTool(self):
		chunkSize = int(self.cmdLineEdit.currentText(), 0)
		self._updateMru()
		self.treeView.clear()
		if not self.hexview: return
		for i,buf in enumerate(self.hexview.buffers):
			root = QTreeWidgetItem(self.treeView)
			root.setText(0, "Buffer %d: %r" % (i, buf.metadata))
			root.setExpanded(True)
			for chunk in range(0, len(buf.buffer), chunkSize):
				x = QTreeWidgetItem(root)
				chunkEnd = min(chunk + chunkSize, len(buf.buffer))
				entropy = calcEntropy(buf.buffer[chunk:chunkEnd])
				x.setText(0, "0x%x - 0x%x" % (chunk, chunkEnd - 1, ))
				x.setText(1, "%0.02f" % (entropy, ))
				x.setText(2, "#" * round(entropy * 10))
				x.setData(0, QtCore.Qt.UserRole, Range(chunk, chunkEnd, buffer_idx=i))

	def _currentItemChanged(self, item, prevItem):
		if not item: return
		range = item.data(0, QtCore.Qt.UserRole)
		if not range: return
		self.hexview.selectRange(range, True)


def calcEntropy(buffer):
	from collections import defaultdict
	from math import log

	counts = defaultdict(lambda: 0)
	for byte in buffer:
		counts[byte] += 1

	result = 0.0
	length = len(buffer)

	for i in counts.values():
		frequency = i / length
		result -= frequency * (log(frequency) / log(2))

	return round(result / 8, 4)

