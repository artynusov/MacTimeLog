# 
#  GraphView.py
#  View for displaying charts
#  `
#  Copyright 2009 Artem Yunusov. All rights reserved.
# 
from Foundation import *
from AppKit import *
from Charts import CocoaHorizontalBarChart, Bar, Header

class GraphView(NSView):
    """View for displaying Charts"""
    _data = []
    _scale = 10
    
    _convFunction = None
    scrollView = None
    
    def initWithFrame_(self, frame):
        self = super(GraphView, self).initWithFrame_(frame)
        if self:
            pass
        return self
        
    def _fillBackground(self, width, height):
        NSColor.colorWithCalibratedRed_green_blue_alpha_(0.95,0.95,0.95, 1.0).setFill()
        drawingPath = NSBezierPath.bezierPath()
        drawingPath.appendBezierPathWithRect_(NSMakeRect(1, 1, width - 2, height - 2))
        drawingPath.fill()

    def isFlipped(self):
        return True
        
    def setScrollView(self, sv):
        self.scrollView = sv
        
    def setData(self, rawData, dataType):
        data = []
        
        oliveGradient = ((0.90,0.92,0.85, 1.0), (0.81,0.83,0.76, 1.0))
        grayGradient = ((0.6,0.6,0.6, 1.0), (0.70,0.70,0.70, 1.0))
        someGradient = ((0.90,0.71,0.54, 0.9), (1.,0.81,0.64, 0.9))
        
        getColor = lambda t: oliveGradient if t =="work" else grayGradient
        
        if dataType == "tasks":
            for k in rawData.keys():
                data.append(Header(k))
                for task, sec in rawData[k]:
                    data.append(Bar(task, sec, gradient=oliveGradient))
        else:
            for task, sec in rawData:
                gradient = someGradient if dataType == "projects" else grayGradient
                data.append(Bar(task.replace("**", ""), sec, gradient=gradient))
                
        self._data = data
        
    def setScale(self, scale):
        self._scale = scale
        
    def setConversionFunction(self, conv):
        self._convFunction = conv
        
    def drawRect_(self, rect):
        width = self.frame().size.width
        height = self.frame().size.height
        
        self._fillBackground(width, height)
        
        chart = CocoaHorizontalBarChart(width, self._scale)
        
        if self._convFunction:
            chart.setConversionFunction(self._convFunction)
            
        chart.setData(self._data)
        
        chart.draw()
        
        if chart.height() >= height:
            b = self.frame()
            self.setFrame_(NSMakeRect(b.origin.x, b.origin.y, b.size.width, chart.height()))
        elif self.scrollView:
            b = self.scrollView.frame()
            self.setFrame_(NSMakeRect(b.origin.x, b.origin.y, b.size.width-20, b.size.height-10))
            
        self.setNeedsDisplay_(True)

        