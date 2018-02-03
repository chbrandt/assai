# -*- coding:utf-8 -*-
'''
Define the base interface for plot class
'''

from astropy.units import Quantity as _Quantity
class Quantity(_Quantity):
    '''
    Customization of Astropy's Quantity
    '''
    def tolist(self):
        return self.value.tolist()
    # def __init__(self,coord,unit):
    #     self.q = Quantity(coord,unit)
    #
    # @property
    # def value(self):
    #     return self.q.value
    #
    # @property
    # def unit(self):
    #     return self.q.unit
    #
    # def set_value(self,value):
    #     assert isinstance(value,(float,int))
    #     _unit = self.q.unit
    #     self.q = Quantity(value,_unit)
    #
    # def set_unit(self,unit):
    #     assert isinstance(unit,(str,Unit))
    #     _newQ = self.q.to(unit)
    #     self.q = _newQ
    #
    # def asunit(self,unit):
    #     _q = self.q.to(unit,equivalencies=spectral())
    #     return _q
