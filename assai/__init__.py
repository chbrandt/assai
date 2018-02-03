from __future__ import absolute_import
import sys

from .plot import plot
from .plot import element
from .search import xmatch_object, xmatch_position

def hello_world():
    pass

class Assai(object):
    plot = None
    catalogs = None

    def __init__(self):
        self.catalogs = ['first', 'wise', 'sdss', 'galex', 'hers', 'xmm']
        self.init_plot()
        self.syspath_bug = sys.path[:]

    def init_plot(self):
        from bokeh.layouts import column
        p = plot.SED('SED')
        p.draw()
        control = self.setup_control()
        panel = column(control,p._layout)
        self.plot = panel

    def setup_control(self):
        #from bokeh.models.widgets import Div
        #div = Div(text="""bla""",width=20, height=10)

        from bokeh.models.widgets import TextInput
        text = TextInput(value="3c279")

        #from bokeh.models.widgets import RadioGroup
        #group = RadioGroup(labels=["object", "position"], active=0, inline=True)

        def research(*args,**kwargs):
            sys.path = self.syspath_bug
            t = text.value
            p = plot.SED(t)
            self.search_object(t, p)
            p.draw()
            self.plot.children[1] = p._layout

        from bokeh.models import Button
        btn = Button(label='search', button_type='success')
        btn.on_click(research)

        js_download = """
            var csv = source.data;
            var filetext = 'catalog,flux,freq\\n';
            for (i=0; i < csv['catalog'].length; i++) {
                var currRow = [csv['catalog'][i].toString(),
                               csv['flux'][i].toString(),
                               csv['freq'][i].toString().concat('\\n')];
                
                var joined = currRow.join();
                filetext = filetext.concat(joined);
            }
             
            var filename = 'results.csv';
            var blob = new Blob([filetext], { type: 'text/csv;charset=utf-8;' });
            if (navigator.msSaveBlob) { // IE 10+
            navigator.msSaveBlob(blob, filename);
            } else {
            var link = document.createElement("a");
            if (link.download !== undefined) { // feature detection
                // Browsers that support HTML5 download attribute
                var url = URL.createObjectURL(blob);
                link.setAttribute("href", url);
                link.setAttribute("download", filename);
                link.style.visibility = 'hidden';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            }
            }"""

        from bokeh.models import ColumnDataSource
        source = ColumnDataSource({'catalog':['a','b','c'],'flux':[1,2,3],'freq':[1,2,3]})

        from bokeh.models import Button
        btn2 = Button(label='download', button_type='success')
        from bokeh.models.callbacks import CustomJS
        btn2.callback = CustomJS(args=dict(source=source), code=js_download)

        from bokeh.layouts import column,row
        return row(text,btn, btn2)

    def show(self):
        from bokeh.io import show
        show(self.plot)

    def search_object(self, obj, plot):
        data = xmatch_object(obj, radius=5, catalogs=self.catalogs)
        ingest_data(data, plot)

    @property
    def layout(self):
        return self.plot


def ingest_data(data, plot):
    if data is not None:
        assert all(col in data.columns for col in ['catalog','flux','freq'])
        for survey,group in data.groupby('catalog'):
            el = element.Element(survey,group,y='flux',x='freq')
            plot.add_element(el)



#    sed = plot.SED('SED')
#
#    flux_table = search_object(object_name, radius=5, catalogs=catalogs)
#    cols = flux_table.columns
#
#    for survey,group in flux_table.groupby('catalog'):
#        #     print(survey)
#        #     print(group)
#        el = element.Element(survey,group,y='flux',x='freq')
#        sed.add_element(el)
#
#    # sed.draw()
#    # sed.show()
#    sed.plot()
#
