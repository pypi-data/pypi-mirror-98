#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2021 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkWidgets.widget import *
from TermTk.TTkWidgets.frame import *

class TTkSplitter(TTkFrame):
    __slots__ = ('_splitterInitialized', '_orientation','_separators', '_separatorSelected', '_mouseDelta')
    def __init__(self, *args, **kwargs):
        self._splitterInitialized = False
        # self._splitterInitialized = True
        self._separators = []
        self._separatorSelected = None
        self._orientation = TTkK.HORIZONTAL
        TTkFrame.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkSpacer')
        self._orientation = kwargs.get('orientation', TTkK.HORIZONTAL)
        self.setBorder(False)
        self.setFocusPolicy(TTkK.ClickFocus)
        self._splitterInitialized = True

    def addWidget(self, widget, size=None):
        TTkFrame.addWidget(self, widget)
        _,_,w,h = self.geometry()

        if self._orientation == TTkK.HORIZONTAL:
            fullSize = w
        else:
            fullSize = h

        if self._separators:
            newSep = (self._separators[-1] + fullSize)  // 2
        else:
            newSep = -1
        self._separators.append(newSep)
        self._updateGeometries()

    def _minMaxSizeBefore(self, index):
        if self._separatorSelected is None:
            return 0, 0x1000
        # this is because there is a hidden splitter at position -1
        minsize = -1
        maxsize = -1
        for i in range(self._separatorSelected):
            item = self.layout().itemAt(i)
            minsize += item.minDimension(self._orientation)+1
            maxsize += item.maxDimension(self._orientation)+1
        return minsize, maxsize

    def _minMaxSizeAfter(self, index):
        if self._separatorSelected is None:
            return 0, 0x1000
        minsize = 0x0
        maxsize = 0x0
        for i in range(self._separatorSelected, len(self._separators)):
            item = self.layout().itemAt(i)
            minsize += item.minDimension(self._orientation)+1
            maxsize += item.maxDimension(self._orientation)+1
        return minsize, maxsize

    def _updateGeometries(self):
        _,_,w,h = self.geometry()
        sep = self._separators
        x,y=0,0

        def _processGeometry(index, forward):
            item = self.layout().itemAt(i)

            if self._orientation == TTkK.HORIZONTAL:
                newPos  = sep[i]+1
                size = w-newPos
            else:
                newPos = sep[i]+1
                size = h-newPos

            if i<=len(sep)-2: # this is not the last widget
                size = sep[i+1]-newPos
                maxsize = item.maxDimension(self._orientation)
                minsize = item.minDimension(self._orientation)
                if   size > maxsize: size = maxsize
                elif size < minsize: size = minsize
                if forward:
                    sep[i+1]=sep[i]+size+1
                else:
                    sep[i]=sep[i+1]-size-1

            if self._orientation == TTkK.HORIZONTAL:
                item.setGeometry(sep[i]+1,0,size,h)
            else:
                item.setGeometry(0,sep[i]+1,w,size)
            pass


        selected = 0
        if self._orientation == TTkK.HORIZONTAL:
            size = w
        else:
            size = h
        if self._separatorSelected is not None:
            selected = self._separatorSelected
            sepPos = sep[selected]
            minsize,maxsize = self._minMaxSizeBefore(selected)
            # TTkLog.debug(f"before:{minsize,maxsize}")
            if sepPos > maxsize: sep[selected] = maxsize
            if sepPos < minsize: sep[selected] = minsize
            minsize,maxsize = self._minMaxSizeAfter(selected)
            # TTkLog.debug(f"after:{minsize,maxsize}")
            if sepPos < size-maxsize: sep[selected] = size-maxsize
            if sepPos > size-minsize: sep[selected] = size-minsize

        forward = False
        for i in reversed(range(selected)):
            _processGeometry(i, False)

        forward = True
        for i in range(selected, len(sep)):
            _processGeometry(i, True)

    def resizeEvent(self, w, h):
        self._updateGeometries()

    def paintEvent(self):
        w,h = self.size()
        if self._orientation == TTkK.HORIZONTAL:
            for i in self._separators:
                self._canvas.drawVLine(pos=(i,0), size=h)
        else:
            for i in self._separators:
                self._canvas.drawHLine(pos=(0,i), size=w)

    def mousePressEvent(self, evt):
        self._separatorSelected = None
        self._mouseDelta = (evt.x, evt.y)
        x,y = evt.x, evt.y
        # TTkLog.debug(f"{self._separators} {evt}")
        for i in range(len(self._separators)):
            val = self._separators[i]
            if self._orientation == TTkK.HORIZONTAL:
                if x == val:
                    self._separatorSelected = i
                    self.update()
                    self._updateGeometries()
            else:
                if y == val:
                    self._separatorSelected = i
                    self.update()
                    self._updateGeometries()
        return self._separatorSelected is not None

    def mouseDragEvent(self, evt):
        if self._separatorSelected is not None:
            if self._orientation == TTkK.HORIZONTAL:
                self._separators[self._separatorSelected] = evt.x
            else:
                self._separators[self._separatorSelected] = evt.y
            self._updateGeometries()
            self.update()
            return True
        return False

    def focusOutEvent(self):
        self._separatorSelected = None

    def minimumHeight(self) -> int:
        if not self._splitterInitialized: return 0
        min = 0
        if self._orientation == TTkK.VERTICAL:
            for item in self.layout().children():
                min+=item.minimumHeight()
        else:
            for item in self.layout().children():
                if min < item.minimumHeight():
                    min = item.minimumHeight()
        return min

    def minimumWidth(self)  -> int:
        if not self._splitterInitialized: return 0
        min = 0
        if self._orientation == TTkK.HORIZONTAL:
            for item in self.layout().children():
                min+=item.minimumWidth()
        else:
            for item in self.layout().children():
                if min < item.minimumWidth():
                    min = item.minimumWidth()
        return min

    def maximumHeight(self) -> int:
        if not self._splitterInitialized: return 0x10000
        if self._orientation == TTkK.VERTICAL:
            max = 0
            for item in self.layout().children():
                max+=item.maximumHeight()
        else:
            max = 0x10000
            for item in self.layout().children():
                if max > item.maximumHeight():
                    max = item.maximumHeight()
        return max

    def maximumWidth(self)  -> int:
        if not self._splitterInitialized: return 0x10000
        if self._orientation == TTkK.HORIZONTAL:
            max = 0
            for item in self.layout().children():
                max+=item.maximumHeight()
        else:
            max = 0x10000
            for item in self.layout().children():
                if max > item.maximumWidth():
                    max = item.maximumWidth()
        return max
