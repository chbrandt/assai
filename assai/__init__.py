from __future__ import absolute_import

from plot import plot
from plot import element
from sed_builder import search_object, search_position

def hello_world():
    pass

class Assai(object):
    plot = None
    catalogs = None

    def __init__(self):
        self.catalogs = ['first', 'wise', 'sdss', 'galex', 'hers', 'xmm']
        self.setup_plot()

    def setup_control(self):
        from bokeh.models.widgets import Div
        div = Div(text="""bla""",width=20, height=10)

        from bokeh.models.widgets import TextInput
        text = TextInput(value="3c279")

        from bokeh.models.widgets import RadioGroup
        group = RadioGroup(labels=["object", "position"], active=1, inline=True)

        def func(*args,**kwargs):
            t = text.value
            if not group.active:
                p = plot.SED(t)
                self.search(t, p)
                p.draw()
                self.plot.children[1] = p._layout
            div.text = t

        from bokeh.models import Button
        btn = Button(label='search', button_type='success')
        btn.on_click(func)

        def down(*args,**kwargs):
            content = 'yay'
            div2 = Div(text=content,width=20, height=10)
            from bokeh.io import show
            from bokeh.layouts import widgetbox
            show(widgetbox(div2))
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
        return row(column(text,group),btn, div, btn2)

    def setup_plot(self):
        from bokeh.layouts import column
        p = plot.SED('SED')
        self.search('mrk421', p)
        p.draw()
        control = self.setup_control()
        panel = column(control,p._layout)
        self.plot = panel

    def show(self):
        from bokeh.io import show
        show(self.plot)

    def search(self, name, plot):
        data = search_object(name, radius=5, catalogs=self.catalogs)
        for survey,group in data.groupby('catalog'):
            el = element.Element(survey,group,y='flux',x='freq')
            plot.add_element(el)

    @property
    def layout(self):
        return self.plot



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
