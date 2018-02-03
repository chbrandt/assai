from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.io import show, output_notebook
from bokeh.models import ColumnDataSource, Button, CustomJS
from bokeh.layouts import column

# setup plot
fig = figure(title='Select points',
            plot_width=300, plot_height=200)

import numpy as np
x = np.linspace(0,10,100)
y = np.random.random(100) + x

import pandas as pd
data = pd.DataFrame(dict(x=x, y=y))

# define data source
src = ColumnDataSource(data)

# define plot
fig.circle(x='x', y='y', source=src)

# define interaction
def print_datapoints(attr, old, new):
    with open('/tmp/datapoints.json', 'w') as f:
        import json
        json.dump(src.selected, f)

btn = Button(label='Selected points', button_type='success')
btn.on_click(print_datapoints)

curdoc().add_root(column(btn,fig))
