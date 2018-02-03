from .base import BaseComponent
class PanelBase(BaseComponent):
    _widgetbox = None
    _elements = None
    def __init__(self,label):
        super(PanelBase,self).__init__(label=label)
        self.create_elements('elements')

    def create_widgetbox(self,widgets):
        from bokeh.layouts import widgetbox
        self._widgetbox = widgetbox(widgets)

    def create_elements(self,label):
        self._elements = []

    def add_element(self,element):
        self._elements.append(element)

    def add_control(self,control):
        pass
    def remove_control(self,label):
        pass
