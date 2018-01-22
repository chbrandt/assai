from astropy.units import Quantity

class Catalog(object):
    def __init__(self,label,table,filters,columns_2_filters,columns_2_position):
        self.label = label
        self.table = table
        self.photo = filters
        self._MAPS = columns_2_filters
        self._MPOS = columns_2_position

    def __str__(self):
        return "{}\n{}".format(str(self.photo),str(self.table))

    def __repr__(self):
        return str(self)

    def __bool__(self):
        if self.table is not None:
            return bool(len(self.table))
        return False

    def xmatch(self,ra,dec,compare=None,inplace=True):
        def default_compare(ra,dec,racol,decol):#ra_target,dec_target,ra_candidates,dec_candidates):
            import numpy as np
            from astropy.coordinates import SkyCoord
            from astropy import units
            c = SkyCoord(ra=ra*units.degree, dec=dec*units.degree)
            cat = SkyCoord(ra=racol, dec=decol,unit=units.degree)
            # idx, d2d, d3d = c.match_to_catalog_sky(cat)
            d2d = c.separation(cat)
            return [np.argmin(d2d)]
        compare = compare or default_compare
        _racol = self._MPOS['ra']
        _decol = self._MPOS['dec']
        _racol = self.table[_racol]
        _decol = self.table[_decol]
        inds = compare(ra,dec,_racol,_decol)
        tab = self.table[inds]
        self.table = tab

    def flux_table(self,frequency_unit=None):
        tab = self.fluxes()
        df = tab.to_pandas().T
        wls = self.wavelengths(unit=frequency_unit)
        freqname = "freq({})".format(wls.unit)
        df[freqname] = wls.value
        return df

    def fluxes(self,unit='erg s-1 cm-2',nufnu=True):
        #TODO: output a pandas dataframe
        out = self.table.copy()
        # for colname in self.table.columns_by_ucd('phot'):
        for colname in self._MAPS:
            out[colname] = self.photo.flux(self.table[colname],
                                            self._MAPS[colname],
                                            unit)
        return out

    def wavelengths(self,unit=None):
        import numpy
        out = []
        for colname in self.table.colnames:
            if colname not in self._MAPS:
                out.append(None)
                continue
            filter_ = self._MAPS[colname]
            wavelength = self.photo.wavelength(filter_,unit)
            out.append(wavelength.value)
            if unit is None:
                unit = wavelength.unit
        out = numpy.array(out,float)
        return Quantity(out,unit)



import numpy as np
from astropy.table import Table, Column
def transpose_table(tab_before, id_col_name='ID'):
    '''Returns a copy of tab_before (an astropy.Table) with rows and columns interchanged
        id_col_name: name for optional ID column corresponding to
        the column names of tab_before'''
    # contents of the first column of the old table provide column names for the new table
    # TBD: check for duplicates in new_colnames & resolve
    new_colnames=tuple(tab_before[tab_before.colnames[0]])
    # remaining columns of old table are row IDs for new table
    new_rownames=tab_before.colnames[1:]
    # make a new, empty table
    tab_after=Table(names=new_colnames)
    # add the columns of the old table as rows of the new table
    for r in new_rownames:
        tab_after.add_row(tab_before[r])
    if id_col_name != None:
        # add the column headers of the old table as the id column of new table
        tab_after.add_column(Column(new_rownames, name=id_col_name),index=0)
    return(tab_after)
