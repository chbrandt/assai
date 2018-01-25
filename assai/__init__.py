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
        #self.search_position('0,0', p)
        p.draw()
        control = self.setup_control()
        panel = column(control,p._layout)
        self.plot = panel

    def setup_control(self):
        #from bokeh.models.widgets import Div
        #div = Div(text="""bla""",width=20, height=10)

        from bokeh.models.widgets import TextInput
        text = TextInput(value="3c279")

        from bokeh.models.widgets import RadioGroup
        group = RadioGroup(labels=["object", "position"], active=0, inline=True)

        def research(*args,**kwargs):
            sys.path = self.syspath_bug
            t = text.value
            p = plot.SED(t)
            if group.active:
                self.search_position(t,p)
            else:
                self.search_name(t, p)
            p.draw()
            self.plot.children[1] = p._layout

        from bokeh.models import Button
        btn = Button(label='search', button_type='success')
        btn.on_click(research)

        js_download = """
            var filetext = 'itemnum,storename,date,usage,netsales\\n';
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

        from bokeh.models import Button
        btn2 = Button(label='download', button_type='success')
        from bokeh.models.callbacks import CustomJS
        btn2.callback = CustomJS(code=js_download)

        from bokeh.layouts import column,row
        return row(column(text,group),btn, btn2)

    def show(self):
        from bokeh.io import show
        show(self.plot)

    def search_position(self, pos, plot):
        pos_ = pos.split(',')
        if len(pos_) == 1:
            pos_ == pos.split()
        try:
            ra,dec = [float(p.strip()) for p in pos_]
        except:
            msg = "Expecting string of 'ra_j2000, dec_j2000' values, instead got '{}'"
            raise ValueError(msg.format(pos))
        data = xmatch_position(ra, dec, radius=5, catalogs=self.catalogs)
        ingest_data(data, plot)

    def search_name(self, name, plot):
        data = xmatch_object(name, radius=5, catalogs=self.catalogs)
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
