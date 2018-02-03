import bokeh

from .base import BaseComponent
from .axis import AxisBase
from .element import ElementsListBase

TOOLBAR = { 'location' : 'above' }

class PlotBase(BaseComponent):
    _AxisClass = AxisBase
    __ElementClass = ElementsListBase

    _elements = None
    _figure = None
    _xaxis = None
    _yaxis = None

    def __init__(self, label, x_label='x', y_label='y', **kwargs):
        super(PlotBase,self).__init__(label=label)
        self.create_figure(**kwargs)
        self.create_xaxis(label=x_label)
        self.create_yaxis(label=y_label)

        self.create_elements(label='elements')

    def __len__(self):
        return len(self._elements)

    def create_figure(self,**kwargs):
        from bokeh.plotting import figure
        self._figure = figure(title=self.label,
                                toolbar_location=TOOLBAR['location'],
                                toolbar_sticky=False,
                                **kwargs)

    def create_xaxis(self,label):
        self._xaxis = self._AxisClass(label=label,axis=self._figure.xaxis)

    def create_yaxis(self,label):
        self._yaxis = self._AxisClass(label=label,axis=self._figure.yaxis)

    def create_elements(self,label):
        self._elements = self.__ElementClass(label)

    @property
    def figure(self):
        return self._figure

    @property
    def xaxis(self):
        return self._xaxis

    @property
    def yaxis(self):
        return self._yaxis

    @property
    def elements(self):
        return self._elements

    def add_element(self,element):
        self._elements.append(element)
        return len(self) - 1

    def draw(self):
        self._elements.draw(self._figure)

        from bokeh.models import Legend
        legendlist = []
        for element in self._elements:
            legendlist.append( (element.label,[element.glyph]) )
        legend = Legend(items=legendlist, location=(0, -30))
        legend.click_policy="hide"
        self._figure.add_layout(legend,'right')

    def show(self):
        from bokeh.io import show
        show(self._figure)

    def replot(self,**kwargs):
        self.create_figure(x_label=self.xaxis.label,
                            y_label=self.yaxis.label,
                            **kwargs)
        self.draw()
        self.show()

    def set_axes_scale(self,xaxis='linear',yaxis='linear'):
        self.replot(x_axis_type=xaxis,y_axis_type=yaxis)

    def remove_element(self,label=None):
        '''
        If label is None, remove last element added
        '''
        if not len(self._elements):
            return None
        for i,element in enumerate(self._elements):
            if element.label == label:
                break
        _ = self._elements.pop(i)
        self.replot()
