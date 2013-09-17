#
#  charts.py
#  Classes for drawing charts
#
#  Copyright 2009 Artem Yunusov. All rights reserved.
#

from Foundation import *
from AppKit import *


class Bar(object):
    """Bar class"""
    def __init__(self, title, value, color=None, gradient=None):
        self.title = title
        self.value = value
        self.color = color
        self.gradient = gradient


class Header(object):
    """Header class"""

    def __init__(self, title):
        self.title = title


class HorizontalBarChart(object):
    """Basic Bar Chart logic"""

    def __init__(self, chartWidth, scaleSize):
        self._rightSpace = 80
        self._bottomSpace = 10
        self._topSpace = 15
        self._scaleSize = scaleSize
        self._chartWidth = chartWidth
        self._scaleIndex = 1
        self._data = []
        self._barHeight = 20
        self._currentYPos = 0 + self._topSpace
        self._barXPos = 100
        self._textXPos = 10
        self._barSpace = 10
        self._barTextSpace = 20
        self._conv = lambda v: str(v)

    def _countBarSize(self, value):
        """Return Bar width in pixels taking in account it's value"""
        return round((self._chartWidth-self._barXPos - self._rightSpace) /
                (float(self._scaleSize) / float(value)))

    def _prepareValue(self, value):
        """Apply conversion function to value before displaying it"""
        return self._conv(value)

    def draw(self):
        """Draw Chart"""
        for obj in self._data:
            if isinstance(obj, Bar):
                self._currentYPos += self._barSpace
                self._drawBar(obj)
                self._currentYPos += self._barHeight
            elif isinstance(obj, Header):
                self._drawHeader(obj)

    def height(self):
        """Chart height"""
        return self._currentYPos + self._bottomSpace

    def width(self):
        """Chart weight"""
        return self._chartWidth

    def setData(self, data):
        """Set Chart data"""
        self._data = data
        self._barXPos = (self._prepareBarAttributes() +
                self._textXPos + self._barTextSpace)

    def setConversionFunction(self, conv):
        """Set conversion function that will be called before displaying value"""
        self._conv = conv

    def _prepareBarAttributes(self):
        """
        Prepare Bar.title and Bar.value for drawing,
        will be overwritten in child class, returns max title width

        """
        return self._barXPos


class CocoaHorizontalBarChart(HorizontalBarChart):
    """
    Class which implements Bar Chart for Cocoa
    """

    _shadow = NSShadow.alloc().init()

    def _prepareBarAttributes(self):
        """Prepare Bar.title and Bar.value for drawing"""
        maxWidth = 0
        for obj in self._data:
            if isinstance(obj, Bar):
                stringAttributes = {
                    NSFontAttributeName: NSFont.fontWithName_size_(
                            "Helvetica", 12),
                }

                obj.prepTitle = NSAttributedString.alloc(). \
                                         initWithString_attributes_(obj.title,
                                                stringAttributes)
                maxWidth = max(maxWidth, obj.prepTitle.size().width)

                stringAttributes[NSForegroundColorAttributeName] = \
                            NSColor.colorWithCalibratedRed_green_blue_alpha_(
                                    0.3, 0.3, 0.3, 1.0)

                obj.prepValue = (NSAttributedString.alloc().
                            initWithString_attributes_(self._prepareValue(
                                obj.value), stringAttributes))
        return maxWidth

    def _dropShadows(self):
        """Switch on shadow"""
        shadow = self._shadow
        shadow.setShadowColor_(NSColor.blackColor().colorWithAlphaComponent_(
                0.3))
        shadow.setShadowOffset_(NSMakeSize(4.0, -4.0))
        shadow.setShadowBlurRadius_(3.0)
        shadow.set()

    def _offShadow(self):
        """Switch off shadow"""
        self._shadow = NSShadow.alloc().init()
        self._shadow.set()

    def _gradient(self, path, color1, color2):
        """Apply gradient"""
        startingColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(*color1)
        endingColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(*color2)
        gradient = NSGradient.alloc().initWithStartingColor_endingColor_(
                startingColor, endingColor)
        gradient.drawInBezierPath_angle_(path, 90)

    def _drawHeader(self, header):
        """Draw header"""
        stringAttributes = {
            NSFontAttributeName: NSFont.fontWithName_size_("Helvetica", 15),
        }
        self._offShadow()
        headerStr = NSAttributedString.alloc().initWithString_attributes_(
                header.title, stringAttributes)
        self._currentYPos += self._barSpace

        headerStr.drawAtPoint_(NSMakePoint(self._barXPos, self._currentYPos))
        self._currentYPos += headerStr.size().height

    def _drawBar(self, bar):
        """Draw bar with label"""
        barLength = self._countBarSize(bar.value)
        self._offShadow()

        textYPos = int(round((
                self._barHeight - bar.prepTitle.size().height) / 2.0))
        bar.prepTitle.drawAtPoint_(NSMakePoint(self._textXPos,
                textYPos + self._currentYPos))

        bar.prepValue.drawAtPoint_(NSMakePoint(self._barXPos + barLength + 10,
                textYPos + self._currentYPos))

        self._dropShadows()

        NSColor.blackColor().setStroke()

        if bar.color:
            NSColor.colorWithCalibratedRed_green_blue_alpha_.setFill(bar.color)

        drawingPath = NSBezierPath.bezierPath()
        drawingPath.appendBezierPathWithRect_(NSMakeRect(self._barXPos,
                self._currentYPos, barLength, self._barHeight))
        drawingPath.stroke()
        drawingPath.fill()

        if bar.gradient:
            self._gradient(drawingPath, *bar.gradient)
