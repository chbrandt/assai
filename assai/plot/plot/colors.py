def palette(self,palette_type=None,size=None):
    '''
    Types of palette: 'categorical', 'continuous', 'spectral'
    '''
    from bokeh import palettes
    if palette_type is None:
        palette_type = 'categorical'

    if palette_type == 'categorical':
        size = int(size)
        palette = palettes.Colorblind8
        palette.extend(palettes.Category20_20)
        return palette[size]
    elif palette_type == 'continuous':
        from bokeh.palettes import viridis,magma
        _vir = viridis(self.NUMAX)
        _mag = magma(self.NUMAX)
        colors = _mag[:]
        colors[1::2] = _vir[1::2]
        from random import shuffle,seed
        seed(1234567)
        shuffle(colors)
    else:
        pass
    self.palette = colors[:]

def _get_color(self,ds_label):
    ds_index = self.datasources[ds_label].get('index')
    return self.palette[ds_index]
