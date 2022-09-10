"""
This plugin is an example for a custom DockWidget, it displays an analog clock.

Actual clock rendering is based on example code from:
https://www.geeksforgeeks.org/create-analog-clock-using-pyqt5-in-python/
"""

import logging

import pre_workbench.app
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QTimer, QPoint, QTime
from PyQt5.QtGui import QPolygon, QPainter, QBrush, QPen, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from pre_workbench.controls.scintillaedit import ScintillaEdit
from pre_workbench.typeregistry import DockWidgetTypes

@DockWidgetTypes.register(title="Clock", icon="alarm-clock.png", showFirstRun=True, dock="Left")
# creating a clock class
class Clock(QWidget):

    # constructor
    def __init__(self):
        super().__init__()

        # creating a timer object
        timer = QTimer(self)

        # adding action to the timer
        # update the whole code
        timer.timeout.connect(self.update)

        # setting start time of timer i.e 1 second
        timer.start(1000)

        # setting window title
        self.setWindowTitle('Clock')

        # setting window geometry
        self.setGeometry(200, 200, 300, 300)

        # creating hour hand
        self.hPointer = QtGui.QPolygon([QPoint(6, 7),
                                        QPoint(-6, 7),
                                        QPoint(0, -50)])

        # creating minute hand
        self.mPointer = QPolygon([QPoint(6, 7),
                                  QPoint(-6, 7),
                                  QPoint(0, -70)])

        # creating second hand
        self.sPointer = QPolygon([QPoint(1, 1),
                                  QPoint(-1, 1),
                                  QPoint(0, -90)])
        # colors
        # color for minute and hour hand
        self.bColor = QtCore.Qt.white

        # color for second hand
        self.sColor = QtCore.Qt.green

        # background color
        self.bgColor = QColor("#111111")

    # method for paint event
    def paintEvent(self, event):

        # getting minimum of width and height
        # so that clock remain square
        rec = min(self.width(), self.height())

        # getting current time
        tik = QTime.currentTime()

        # creating a painter object
        painter = QPainter(self)
        painter.fillRect(0, 0, self.width(), self.height(), self.bgColor)

        # method to draw the hands
        # argument : color rotation and which hand should be pointed
        def drawPointer(color, rotation, pointer):

            # setting brush
            painter.setBrush(QBrush(color))

            # saving painter
            painter.save()

            # rotating painter
            painter.rotate(rotation)

            # draw the polygon i.e hand
            painter.drawConvexPolygon(pointer)

            # restore the painter
            painter.restore()


        # tune up painter
        painter.setRenderHint(QPainter.Antialiasing)

        # translating the painter
        painter.translate(self.width() / 2, self.height() / 2)

        # scale the painter
        painter.scale(rec / 200, rec / 200)

        # set current pen as no pen
        painter.setPen(QtCore.Qt.NoPen)


        # draw each hand
        drawPointer(self.bColor, (30 * (tik.hour() + tik.minute() / 60)), self.hPointer)
        drawPointer(self.bColor, (6 * (tik.minute() + tik.second() / 60)), self.mPointer)
        drawPointer(self.sColor, (6 * tik.second()), self.sPointer)


        # drawing background
        painter.setPen(QPen(self.bColor))

        # for loop
        for i in range(0, 60):

            # drawing background lines
            if (i % 5) == 0:
                painter.drawLine(87, 0, 97, 0)

            # rotating the painter
            painter.rotate(6)

        # ending the painter
        painter.end()

