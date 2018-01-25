#!/usr/bin/env python

from bokeh.io import curdoc,show

from assai import Assai

sed = Assai()

if __name__ == '__main__':
    show(sed.layout)
else:
    curdoc().add_root(sed.layout)

