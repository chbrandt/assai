#!/usr/bin/env python
from __future__ import absolute_import, print_function

import warnings
warnings.simplefilter('ignore')

import logging
#logging.basicConfig(level=logging.ERROR)

# I here include the place where the catalogs are defined
#
import os
_here = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.insert(0, os.path.join(_here, 'catalogs'))

# Catalogs -- as packages -- must provide a 'search' function,
# informations about filters (wavelengths) associated to their
# flux columns
# The Catalog and Filter classes are for...
#
from catalogs.core import Catalog
from catalogs.filters import Filter


#_CATALOGS = ['first', 'wise', 'sdss', 'galex', 'hers', 'xmm']
#_RADIUS = 1E-3 #degree


def search_catalog(ra, dec, radius, catalog_name):
    """
    Return a `Catalog` instance with retrieved data

    Input:
     - ra,dec : coordinates in degree units
     - radius : float or astropy.Angle
        If float, it is assumed a value in 'arcsec' units
    """
    from importlib import import_module
    mod = import_module(catalog_name)

    try:
        radius = radius.degree
    except:
        radius = float(radius)/3600

    # Query catalog data
    tab = mod.search(ra,dec,radius)

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


def search_position(ra, dec, radius, catalogs):
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

    for catalog in catalogs:

        print('Searching catalog: {}'.format(catalog))
        cat = search_catalog(ra, dec, radius, catalog)

        if not cat:
            print("> Failed to query/retrieve data")
            continue
        print("> {:d} objects found".format(len(cat.table)))

        _ = cat.xmatch(ra,dec)

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


def search_object(name, radius, catalogs):

    # Get the object's coordinates
    #
    from catalogs.tools import resolve_name
    pos = resolve_name(name)
    if pos:
        ra,dec = pos
        logging.info("Object '{}' RA,Dec: {},{}".format(name,ra,dec))
    else:
        logging.error("Object {} could not be resolved.".format(name))
        return None

    sed_tab = search_position(ra, dec, radius, catalogs)
    return sed_tab


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--radius', type=float, default=5,
                        help="Search radius (arc seconds)")
    parser.add_argument('object', type=str,
                        help="Name of the object to search")
    args = parser.parse_args()

    import catalogs
    cats = catalogs.__all__

    sed_tab = search_object(args.object, args.radius, cats)

    if sed_tab is None:
        print('SED table returned null')
        sys.exit(1)

    print("\nFinal flux table:")
    print(sed_tab)

