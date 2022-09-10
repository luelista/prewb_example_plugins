
from pre_workbench.controls.hexview_selheur import SelectionHelpers, rangeBefore
from PyQt5.QtGui import QColor, QPen, QPainter
from math import ceil

@SelectionHelpers.register(color="#aa11dd", defaultEnabled=False)
def highlightRainbowPlugin(editor, qp, bbuf, sel, options):
	"""
	This test highlighter draws a rainbow below six bytes starting
	from the beginning of the selection.

	It is loaded from a plugin.
	"""

	(bufIdx, start, end) = sel

	i=start
	len=ceil((end-start+1)/6)
	editor.highlightMatch(qp, (bufIdx, i, i+len), "", QColor("#ff0000")); i=i+len
	editor.highlightMatch(qp, (bufIdx, i, i+len), "", QColor("#ffaa00")); i=i+len
	editor.highlightMatch(qp, (bufIdx, i, i+len), "", QColor("#ffff00")); i=i+len
	editor.highlightMatch(qp, (bufIdx, i, i+len), "", QColor("#00ff00")); i=i+len
	editor.highlightMatch(qp, (bufIdx, i, i+len), "", QColor("#0000ff")); i=i+len
	editor.highlightMatch(qp, (bufIdx, i, i+len), "", QColor("#aa00ff")); i=i+len





