from .base import BaseComponent

class AxisBase(BaseComponent):
    # _limits = None
    # _scale = None
    _axis = None
    def __init__(self,label,axis):
        self._axis = axis
        super(AxisBase,self).__init__(label=label)

    def set_label(self,label):
        super(AxisBase,self).set_label(label)
        self.set_title(label)

    def set_title(self,title):
        if self.scale == 'log':
            title = 'log( {} )'.format(title)
        self._axis.axis_label = title

    @property
    def scale(self):
        from bokeh.models.axes import LogAxis,LinearAxis
        if isinstance(self._axis[0],LinearAxis):
            return 'linear'
        elif isinstance(self._axis[0],LogAxis):
            return 'log'
        else:
            return 'unknown'

    # def __set_limits(self,limits):
    #     assert len(limits)==2, "Limits should be a pair of values"
    #     assert limits[0]!=limits[1]
    #     self._limits = Limits(min=min(limits),max=max(limits))
    #     # emit limits_changed
    # def __get_limits(self):
    #     return self._limits
    # limits = property(__get_limits,__set_limits,"Axis limits")
