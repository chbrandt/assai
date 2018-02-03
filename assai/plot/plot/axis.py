# -*- coding:utf-8 -*-
'''
Define the base interface for plot class
'''
from .units import Unit,can_convert

from .base.axis import AxisBase
class Axis(AxisBase):
    _unit = None
    def __init__(self,label,axis,unit=''):
        super(Axis,self).__init__(label=label,axis=axis)
        self.set_unit(unit)

    def set_unit(self,unit):
        # print('Setting axis unit. Old:{} , New:{}'.format(self._unit,unit))
        if self._unit is None:
            self._unit = Unit(unit)
        else:
            if can_convert(self._unit,unit):
                self._unit = Unit(unit)
            else:
                print("Unit '{!s}' cannot be converted to '{!s}'".format(self._unit,unit))
        _title = '{!s} [{!s}]'.format(self.label,self.unit)
        self.set_title(_title)

    def get_unit(self):
        return self._unit
    unit = property(get_unit,set_unit,doc="Axis unit")
