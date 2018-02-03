# -*- coding:utf-8 -*-
'''
Define the base interface for plot class
'''
from .axis import Axis
from .element import ElementsList
from .panel import Panel

from .base.plot import PlotBase
class Plot(PlotBase):
    _AxisClass = Axis
    __ElementClass = ElementsList
    _layout = None
    def __init__(self,label,**kwargs):
        # x_unit = kwargs.pop('x_unit') if 'x_unit' in kwargs.keys() else None
        # y_unit = kwargs.pop('y_unit') if 'y_unit' in kwargs.keys() else None
        super(Plot,self).__init__(label=label,**kwargs)
        # self.xaxis.set_unit(x_unit)
        # self.yaxis.set_unit(y_unit)

    def create_figure(self,**kwargs):
        super(Plot,self).create_figure(width=700,height=500,**kwargs)

    def add_element(self,element):
        super(Plot,self).add_element(element)

    def draw(self):
        super(Plot,self).draw()

        from bokeh.layouts import widgetbox,row
        from bokeh.models.widgets import Panel, Tabs

        plot = Panel(child=self._figure, title="Plot")
        table = Panel(child=self._elements.table, title="Table")

        data = widgetbox(Tabs(tabs=[plot,table]),width=800)

        self._layout = row( [data, self._elements.panel] )

    def show(self):
        from bokeh.io import show
        show( self._layout )

    def plot(self):
        self.draw()
        self.show()


class SED(Plot):
    def __init__(self,label='SED'):
        super(SED,self).__init__(label=label,
                                x_label='frequency',
                                y_label='flux',
                                # x_unit='Hz',
                                # y_unit='erg.s-1.cm-2'
                                )

    def create_figure(self,**kwargs):
        super(SED,self).create_figure(x_axis_type='log',
                                      y_axis_type='log',
                                      **kwargs)
