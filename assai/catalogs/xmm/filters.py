# -*- coding:utf8 -*-

"""
Specific definition for XMM data

Things like magnitude-to-flux converstion or filters central wavelength
are meant to be here defined.

Sources:
--------
* esa: http://www.cosmos.esa.int/web/xmm-newton/technical-details-epic
* nasa: https://heasarc.gsfc.nasa.gov/docs/xmm/xmmhp_inst.html
* x-ray comparison: http://space.mit.edu/~jonathan/xray_detect.html
"""
from astropy import units
import logging
import json
import os
_here = os.path.dirname(__file__)

filters = os.path.join(_here, 'filters.json')
with open(filters, 'r') as f:
    filters = json.load(f)


def flux(flxd, band=None, unit=None):
    return flxd


def wavelength(band, unit=None, loc='eff'):
    """
    Returns filter's wavelength according to 'loc' requested

    'band' is the name of the filter: FUV, NUV

    'loc' can be 'min','max' or 'eff', meaning the "minimum",
    "maximum", or "effective" filter wavelength values.
    'central' is accepted as synonym for 'effective'.
    Wavelengths are returned as `~astropy.units.Unit`.
    """
    from astropy import units
    _filters = filters

    assert band in _filters
    fwl = _filters[band].get('wavelength')

    assert loc in fwl
    fwl = fwl[loc] * units.Unit(fwl['unit'])

    if unit is not None:
        unit = units.Unit(unit)
        if unit.is_equivalent(fwl.unit, units.spectral()):
            fwl = fwl.to(unit, equivalencies=units.spectral())

    return fwl
