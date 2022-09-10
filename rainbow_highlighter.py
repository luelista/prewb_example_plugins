from pre_workbench.controls.hexview_selheur import SelectionHelpers, rangeBefore
from PyQt5.QtGui import QColor, QPen, QPainter

@SelectionHelpers.register(color="#aa11dd", defaultEnabled=False)
def highlightRainbowPlugin(editor, qp, bbuf, sel, options):
	"""
	This test highlighter draws a rainbow below six bytes starting
	from the beginning of the selection.

	It is loaded from a plugin.
	"""

	(bufIdx, start, end) = sel
	i=start
	editor.highlightMatch(qp, (bufIdx, i, i+1), "", QColor("#ff0000")); i=i+1
	editor.highlightMatch(qp, (bufIdx, i, i+1), "", QColor("#ffaa00")); i=i+1
	editor.highlightMatch(qp, (bufIdx, i, i+1), "", QColor("#ffff00")); i=i+1
	editor.highlightMatch(qp, (bufIdx, i, i+1), "", QColor("#00ff00")); i=i+1
	editor.highlightMatch(qp, (bufIdx, i, i+1), "", QColor("#0000ff")); i=i+1
	editor.highlightMatch(qp, (bufIdx, i, i+1), "", QColor("#aa00ff")); i=i+1


