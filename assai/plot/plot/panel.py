# -*- coding:utf-8 -*-
'''
Define the base interface for plot class
'''
from .base.panel import PanelBase
class Panel(PanelBase):
    '''
    Implement plot info panel
    '''
    def __init__(self,label):
        super(Panel,self).__init__(label=label)
