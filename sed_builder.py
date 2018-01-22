#!/usr/bin/env python

from __future__ import absolute_import, print_function
import logging

import os
_here = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.insert(0,os.path.join(_here,'catalogs'))

from core import Catalog
from filters import Filter

# _CATALOGS = ['xmm']
_CATALOGS = ['first','wise','sdss','galex','hers','xmm']
_RADIUS = 1E-3 #degree

def search_catalog(ra,dec,catalog_name,search_radius=_RADIUS):
    from importlib import import_module
    mod = import_module(catalog_name)

    # Query catalog data
    tab = mod.search(ra,dec,search_radius)

    # Init catalog filters
    flt = Filter(mod.filters)

    #TODO: implement mapper for table' columns to instrument' filters
    c2f = mod.columns_2_filters

    #TODO: implement mapper for table' columns to position standards
    c2p = mod.columns_2_position

    # 'Catalog' will handle table and its photometric data
    cat = Catalog(label=catalog_name, table=tab, filters=flt,
                    columns_2_filters=c2f, columns_2_position=c2p)

    return cat

def search_waveband(object_name,waveband):
    pass

def search_data(object_name,catalog=None,waveband=None):
    name = object_name
    # Get the object's coordinates
    #
    from tools.bin import resolve_name
    pos = resolve_name.name2coords(object_name)
    if pos:
        ra,dec = pos
        logging.info("Object '{}' RA,Dec: {},{}".format(name,ra,dec))
    else:
        logging.error("Oject {} could not be resolved.".format(object_name))
        return None

    # Init what will be the output table:
    # flux
    # flux_err
    # frequency
    # frequency_width
    # epoch
    # epoch_delta
    #
    def push(table,**kwargs):
        from pandas import DataFrame
        sed_tab = DataFrame(kwargs)
        if table is None:
            return sed_tab
        return table.append(sed_tab)

    # sed_cols=['flux','frequency','catalog']
    sed_tab = None

    catalogs = [catalog] if catalog else _CATALOGS
    for catalog in catalogs:

        cat = search_catalog(ra,dec,catalog,search_radius=0.01)

        if not cat:
            print("> Failed to query/retrieve data")
            continue
        print("> {:d} objects found".format(len(cat.table)))

        _ = cat.xmatch(ra,dec)#ra,dec,flux_tab['ra'],flux_tab['dec'])

        flux_tab = cat.flux_table('Hz')
        flux_tab = flux_tab.dropna()
        cols = flux_tab.columns
        if len(cols) == 0:
            continue

        data = dict(flux = [],
                    freq = [],
                    catalog = catalog)
        frq_col = cols[-1]
        for flx_col in cols[:-1]:
            data['flux'].extend( flux_tab[flx_col] )
            data['freq'].extend( flux_tab[frq_col] )
        sed_tab = push(sed_tab,**data)
    return sed_tab



if __name__ == '__main__':
    import sys
    try:
        object_name = sys.argv[1]
    except:
        print('Usage:\n\t{} <object_name>'.format(os.path.basename(sys.argv[0])))
        sys.exit(1)

    sed_tab = search_data(object_name)
    if sed_tab is None:
        print('SED table returned null')
        sys.exit(1)

    print("\nFinal flux table:")
    print(sed_tab)
