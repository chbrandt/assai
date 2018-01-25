# -*- coding:utf8 -*-

"""
Specific definition for WISE data

Things like magnitude-to-flux converstion or filters central wavelength
are meant to be here defined.

Sources:
--------
* FAQ : http://wise2.ipac.caltech.edu/docs/release/allsky/faq.html
* photometric calibration : http://wise2.ipac.caltech.edu/docs/release/allsky/expsup/sec4_4h.html
* wave and zp : http://coolwiki.ipac.caltech.edu/index.php/Central_wavelengths_and_zero_points
* vo-filters : http://svo2.cab.inta-csic.es/svo/theory/fps3/index.php?mode=voservice
"""

import logging
import json
import os
_here = os.path.dirname(__file__)

filters = os.path.join(_here,'filters.json')
with open(filters,'r') as f:
    filters = json.load(f)

def flux_density(mag,band,unit=None):
    flxd = _mag2fluxdensity(mag,band)
    if unit:
        flxd = flxd.to(unit)
    return flxd

from astropy import units
from astropy.units import Unit

def wavelength(band='full',loc='eff',unit=None):
    """
    Returns filter's wavelength according to 'loc' requested

    'loc' can be 'min','max' or 'eff', meaning the "minimum",
    "maximum", or "effective" filter wavelength values.
    'central' is accepted as synonym for 'effective'.
    Wavelengths are returned as `~astropy.units.Unit`.
    """
    assert band in filters
    # band = band.upper()
    _w = filters[band].get('wavelength')
    assert loc in _w
    _v = _w.get(loc) * Unit(_w['unit'])
    if unit is not None:
        if Unit(unit).is_equivalent(_v.unit,units.spectral()):
            _vv = _v.to(unit,equivalencies=units.spectral())
            _v = _vv
    return _v

def _zeropoint(band):
    """
    Returns Sloan's "asinh" magnitude "b" softening parameter
    """
    assert band in filters
    _zp = filters[band].get('zeropoint')
    assert 'flux' in _zp
    _f = _zp['flux'] * Unit(_zp['unit'])
    return _f

def _mag2fluxdensity(mag,band):
    """
    Converts given magnitude to flux density

    Flux density comes out in 'Jansky' units.
    'filter' is one of UKIRT's {YJHK}.
    """
    import math as m
    mag = mag #* units.mag
    _m = -2.5 #* units.mag
    m_m0 = mag/_m
    f0 = _zeropoint(band)
    f = f0 * m.pow(10,m_m0)
    return f

def _fluxdensity2flux(flux,band):
    from astropy.units import spectral
    freq = wavelength(band).to('Hz',spectral())
    flux = flux.to('mW m-2 Hz-1')
    f_flux = flux * freq
    return f_flux

def _mag2flux(mag,band):
    flux = _mag2fluxdensity(mag,band).to('mW m-2 Hz-1')
    f_flux = _fluxdensity2flux(flux,band)
    return f_flux
