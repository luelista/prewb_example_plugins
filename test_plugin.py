"""
This plugin just shows a hello world message.
"""

from PyQt5.QtWidgets import QMessageBox

QMessageBox.information(None, "Test Plugin", "Hello, world.")
