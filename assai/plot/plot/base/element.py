from .base import BaseComponent
class ElementBase(BaseComponent):
    _x = None
    _y = None
    _data = None

    _style = None
    _color = None
    _board = None

    def __init__(self,label,data,x=None,y=None,properties=None):
        super(ElementBase,self).__init__(label)
        self.__set_data(data,x,y)
        self._board = ElementBoard(self)

    def __set_data(self,data,x,y):
        from bokeh.models import ColumnDataSource
        from pandas import DataFrame
        from numpy import ndarray
        assert any([data is None,
                    len(data) >= 2 if isinstance(data,list) else False,
                    len(data) >= 2 if isinstance(data,dict) else False,
                    data.ndim == 2 if isinstance(data,ndarray) else False,
                    len(data.columns) >= 2 if isinstance(data,DataFrame) else False]),\
                    "We are currently working with 2D data"

        if data is None:
            x = x if x != None else 'x'
            y = y if y != None else 'y'
            data = {x : [],
                    y : []}

        else:
            if isinstance(data,list) or isinstance(data,ndarray):
                inds = list(range(len(data)))
                if x is None or x not in inds:
                    data_x = data[0]
                    x = 'x'
                if y is None or y not in inds:
                    data_y = data[1]
                    y = 'y'
                data = {x : data_x,
                        y : data_y}
            if isinstance(data,dict):
                cols = data.keys()
                if x is None:
                    x = cols[0]
                if y is None:
                    y = cols[1]
            if isinstance(data,DataFrame):
                # Guarantee column names are strings
                data.columns = data.columns.astype(str)
                cols = data.columns
                x = cols[0] if x is None else str(x)
                y = cols[1] if y is None else str(y)
            assert x in data, "'data' has no column '{}'".format(x)
            assert y in data, "'data' has no column '{}'".format(y)
            self._x = x
            self._y = y
        ds = ColumnDataSource(data)
        self._data = ds

    @property
    def datasource(self):
        return self._data

    @property
    def data(self,label=None):
        df = self.datasource.to_df()
        if label is None:
            return df
        return df[label]

    def __get_x(self):
        return self._x
    x = property(__get_x,doc="X-coordinate column name")

    def __get_y(self):
        return self._y
    y = property(__get_y,doc="Y-coordinate column name")

    def __get_style(self):
        return self._style
    def __set_style(self,style):
        self._style = style
    style = property(__get_style,__set_style,doc="Element plot style/symbol")

    def __get_glyph(self):
        return self._glyph
    def __set_glyph(self,glyph):
        self._glyph = glyph
    glyph = property(__get_glyph,__set_glyph,doc="Element plot glyph")

    def __set_color(self,color):
        self._color = color
    def __get_color(self):
        return self._color
    color = property(__get_color,__set_color,doc="Element color")

    def draw(self,fig):
        self._board.draw(fig)
    @property
    def glyph(self):
        return self._board.glyph
    @property
    def panel(self):
        return self._board.panel
    @property
    def table(self):
        return self._board.table



from .base import BaseComponentContainer
class ElementsListBase(BaseComponentContainer):
    '''
    Hold a list of Elements.

    ElementsList controls properties and actions over Elements;
    For example, how colors (palette) will be distributed over elements.
    '''
    _palette = None

    def __init__(self,label,elements=None,palette=None):
        '''
        Input:
         - items   : list of elements (~ElementBase)
         - palette : string
                If None, set the default palette
        '''
        super(ElementsListBase,self).__init__(label=label,items=elements)

    def _can_insert(self,element):
        from numpy import isreal
        return isreal(element.xdata).all() and isreal(element.ydata).all()

    def add_element(self,element):
        if not self._can_insert(element):
            return None
        return super(ElementListBase,self).add(element)

    def set_palette(self,size=None,norm_min=None,norm_max=None,palette_type=None):
        self._palette_type = palette_type

        from bokeh import palettes
        if self._palette_type is None:
            colors = palettes.Colorblind8
            colors.extend(palettes.Category20_20)

            if size and len(colors) < size:
                ns = len(colors) - size
                from bokeh.palettes import viridis,magma
                _vir = viridis(ns)
                _mag = magma(ns)
                _col = _mag[:]
                _col[1::2] = _vir[1::2]
                from random import shuffle,seed
                seed(1234567)
                shuffle(_col)
                colors.extend(_col)

            palette = lambda i:colors[i%len(colors)]
        else:
            self._palette_type = 'spectral'
            norm_min = norm_min if norm_min != None else 0
            norm_max = norm_max if norm_max != None else 1
            from bokeh.palettes import Inferno256,Viridis256
            colors = Inferno256
            colors.extend( Viridis256[::-1] )
            def palette(element,norm_min=norm_min,norm_max=norm_max,colors=colors):
                f = element.x.mean()
                assert norm_min <= f <= norm_max, "Value '{:f}' out of range ({:f},{:f})".format(f,norm_min,norm_max)
                i = int( (len(colors)-1) * (f-norm_min)/(norm_max-norm_min) )
                # print(f,i,norm_min,norm_max,len(colors))
                return colors[i]
        self._palette = palette

    def set_element_color(self,element,i):
        if self._palette_type == 'spectral':
            return self._palette(element)
        else:
            return self._palette(i)

    def draw(self,fig):
        # if self._palette_type == 'spectral':
        #     self.set_palette(norm_min=self.min,norm_max=self.max,palette_type=self._palette_type)
        self.set_palette(len(self))
        for i,element in enumerate(self._items):
            if element.color is None:
                element.color = self.set_element_color(element,i)
            element.draw(fig)
        self._draw_table()
        self._draw_panel()

    def _draw_table(self):
        from bokeh.models.widgets import Panel, Tabs
        tableslist = []
        for i,element in enumerate(self._items):
            tableslist.append( Panel(child=element.table, title=element.label) )
        self.table = Tabs(tabs=tableslist)

    def _draw_panel(self):
        from bokeh.layouts import column
        from bokeh.layouts import widgetbox
        panelslist = []
        for i,element in enumerate(self._items):
            panelslist.append(element.panel)
        self.panel = column(panelslist)



class ElementBoard(object):
    '''
    Control visual interface of an Element

    The board contains a pointer to a table widget,
    corresponding plot glyph and a panel with buttons
    and text widget where info and action can happen.
    '''
    _glyph = None
    _table = None
    _panel = None

    def __init__(self,element):
        self._element = element

    def draw(self,fig):
        self.draw_glyph(fig)
        self._draw_panel()
        self._draw_table()


    @property
    def table(self):
        return self._table

    def _draw_table(self):
        element = self._element
        # from bokeh.layouts import column
        from bokeh.models.widgets import DataTable, TableColumn
        # from bokeh.models.widgets import PreText
        # title = PreText(text=element.label)
        columns = [
            TableColumn(field=element.x, title=element.x),
            TableColumn(field=element.y, title=element.y),
        ]
        table = DataTable(source=element.datasource, columns=columns, width=700, height=400)
        # self._table = column([title,table])
        self._table = table


    @property
    def panel(self):
        return self._panel

    def _draw_panel(self):
        from bokeh.layouts import widgetbox
        from bokeh.models.widgets import Panel, Tabs, Div, CheckboxGroup
        label = Panel( child=CheckboxGroup(labels=[self._element.label], active=[0]), title='label' )
        text = Panel( child=Div(text="""Info text blablabla..."""), title='info' )
        self._panel = Tabs(tabs=[label,text])


    @property
    def glyph(self):
        return self._glyph

    def draw_glyph(self,fig):
        def draw_circle(element,fig):
            return fig.circle(x=element.x, y=element.y, source=element.datasource,
                                name=element.label, color=element.color)
        def draw_square(element,fig):
            return fig.square(x=element.x, y=element.y, source=element.datasource,
                                name=element.label, color=element.color)
        def draw_triangle(element,fig):
            return fig.triangle(x=element.x, y=element.y, source=element.datasource,
                                name=element.label, color=element.color)
        def draw_x(element,fig):
            return fig.x(x=element.x, y=element.y, source=element.datasource,
                                name=element.label, color=element.color)

        STYLES={
                'circle':   draw_circle,
                'square':   draw_square,
                'triangle': draw_triangle,
                None:       draw_circle
                }
        style = self._element.style if self._element.style in STYLES.keys() else None
        renderer = STYLES[style](self._element,fig)
        self._glyph = renderer
