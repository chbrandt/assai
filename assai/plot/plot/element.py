# -*- coding:utf-8 -*-
'''
Define the base interface for plot class
'''
# def fabric(label,x,y,xunit=None,yunit=None):
#     if not (isinstance(x,(tuple,list)) or isinstance(y,(tuple,list))):
#         # It's a "point"
#         return ElementPoint(label,x,y,xunit,yunit)
#     else:
#         # Considered to be a "line"
#         return ElementLine(label,x,y,xunit,yunit)

from .units import init_unit

from .base.element import ElementBase
class Element(ElementBase):
    """
    """

    _xunit = None
    _yunit = None

    _alpha = None
    _weight = None

    def __init__(self,label,data,x=None,y=None,xunit=None,yunit=None):
        super(Element,self).__init__(label=label,data=data,x=x,y=y)
        self.set_xunit(xunit)
        self.set_yunit(yunit)

    def set_xunit(self,unit):
        self._xunit = init_unit(unit)
    def set_yunit(self,unit):
        self._yunit = init_unit(unit)

    def __set_alpha(self,alpha):
        self._alpha = alpha
    def __get_alpha(self):
        return self._alpha
    alpha = property(__get_alpha,__set_alpha,doc="Element alpha")

    def __set_weight(self,weight):
        self._weight = weight
    def __get_weight(self):
        return self._weight
    weight = property(__get_weight,__set_weight,doc="Element weight")



from .base.element import ElementsListBase
class ElementsList(ElementsListBase):
    _xunit = None
    _yunit = None
    def __init__(self,label,elements=None,xunit=None,yunit=None):
        super(ElementsList,self).__init__(label=label,elements=elements)
        self.set_xunit(xunit)
        self.set_yunit(yunit)

    def set_xunit(self,unit):
        _u = init_unit(unit)
        self._xunit = _u

    def set_yunit(self,unit):
        _u = init_unit(unit)
        self._yunit = _u

    def _can_insert(self,element):
        ok = super(ElementList,self)._can_insert(element)
        if not ok:
            return False
        return can_convert(element.xunit,self.xunit) \
                and can_convert(element.yunit,self.yunit)

    def add_element(self,element):
        if not self._can_insert(element):
            return None
        element.xunit_convert(self.xunit, inplace=True)
        element.yunit_convert(self.yunit, inplace=True)
        return super(ElementList,self).add_element(element)




class ElementPoint(Element):
    def __init__(self,label,x,y,xunit=None,yunit=None):
        assert isinstance(x,(float,int))
        assert isinstance(y,(float,int))
        super(ElementPoint,self).__init__(label=label,
                                            x=x,y=y,
                                            xunit=xunit,yunit=yunit)
        self.style = 'circle'

class ElementVector(Element):
    def __init__(self,label,x,y,xunit=None,yunit=None):
        assert len(x)==len(y)
        super(ElementVector,self).__init__(label=label,
                                            x=x,y=y,
                                            xunit=xunit,yunit=yunit)



class ElementCurve(ElementsList):
    '''
    Define a generic curve
    '''
    def __init__(self,label,*points):
        # put points in order
        pts_sorted = sorted(points, key=lambda p:p.x)
        super(ElementCurve,self).__init__(label=label, items=pts_sorted)

class ElementLine(ElementCurve):
    def __init__(self,label,point1,point2):
        assert isinstance(point1,ElementPoint)
        assert isinstance(point2,ElementPoint)
        super(ElementLine,self).__init__(label,x,y,xunit,yunit)

class ElementElipse(Element):
    def __init__(self,label,x,y,semi_major,semi_minor,theta,xunit=None,yunit=None):
        pass

class ElementCircle(ElementElipse):
    def __init__(self,label,x,y,radius):
        pass

class ElementPolygon(Element):
    def __init__(self,label,x,y,xunit=None,yunit=None):
        assert x[0]==x[-1]
        assert y[0]==y[-1]
        pass

class ElementRectangle(ElementPolygon):
    def __init__(self,label,x,y,side_x,side_y,xunit=None,yunit=None):
        signal=lambda x,sim=2:(x//sim)%sim*2-1
        xv = [ x+(side_x/2)*signal(p) for p in range(5) ]
        yv = [ y+(side_y/2)*signal(p) for p in range(5) ]
        super(ElementRectangle,self).__init__(label=label,
                                                x=xv,y=yv,
                                                xunit=xunit,yunit=yunit)

class ElementSquare(ElementRectangle):
    def __init__(self,label,x,y,side,xunit,yunit):
        super(ElementSquare,self).__init__(label=label,
                                            x=x,y=y,side_x=side,side_y=side,
                                            xunit=xunit,yunit=yunit)
