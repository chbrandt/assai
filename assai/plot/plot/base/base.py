# -*- coding:utf-8 -*-
'''
Define the base interface for plot class
'''
from collections import namedtuple
Limits = namedtuple('Limits',['min','max'])

# ID is to be used by every component to uniquely identify
_ID=0

class BaseComponent(object):
    _label = None
    _description = None
    _ID = None

    def __init__(self,label):
        self.set_label(label)
        # Get this object an unique identifier
        global _ID
        _ID += 1
        self._ID = _ID

    @property
    def ID(self):
        return self._ID

    @property
    def label(self):
        return self.get_label()
    def get_label(self):
        return self._label
    def set_label(self,label):
        self._label = label

    def __set_description(self,description):
        self._description = description
    def __get_description(self):
        return self._description
    description = property(__get_description,__set_description,doc="Component description")


class BaseComponentContainer(BaseComponent):
    _items = None
    def __init__(self,label,items=None):
        super(BaseComponentContainer,self).__init__(label)
        self._items = list()
        if items != None:
            if hasattr(items,'__iter__'):
                self.extend(items)
            else:
                self.append(items)

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)

    def add(self,item):
        index = len(self)
        try:
            self._items.append(item)
            return index
        except:
            return None
    append = add

    def item(self,index):
        try:
            return self._items[item]
        except:
            return None

    def get_item(self,label):
        for item in self:
            if label == item.label:
                return item
        return None


class GridBase(BaseComponent):
    _plots = None
    _panel = None
    _table = None
    def add_plot(self,plot,position=None):
        pass
    def remove_plot(self,label,position=None):
        pass
