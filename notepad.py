"""
This plugin is an example for a custom Data Source.

It shows a text editor which automatically stores its contents in the project database.
"""

import logging

import pre_workbench.app
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from pre_workbench.controls.scintillaedit import ScintillaEdit
from pre_workbench.typeregistry import DockWidgetTypes

@DockWidgetTypes.register(title="Notepad", icon="document-text.png", showFirstRun=True)
class NotepadWidget(QWidget):
	def __init__(self):
		super().__init__()
		self._initUI()
		self.editor.setText(pre_workbench.app.CurrentProject.getValue("Notepad", ""))

	def maybeSave(self):
		logging.info("close")
		pre_workbench.app.CurrentProject.setValue("Notepad", self.editor.text())
		return True

	def _initUI(self):
		self.editor = ScintillaEdit()
		windowLayout = QVBoxLayout()
		windowLayout.addWidget(self.editor)
		windowLayout.setContentsMargins(0,0,0,0)
		self.setLayout(windowLayout)
		self.editor.show()
