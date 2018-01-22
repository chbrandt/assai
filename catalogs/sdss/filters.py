"""
Specific definition for Sloan Digital Sky Survey data

Things like magnitude-to-flux converstion or filters central wavelength
are meant to be here defined.

Sources:
--------
* mag-to-flux : http://classic.sdss.org/dr7/algorithms/fluxcal.html
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

def wavelength(band,unit=None,loc='eff'):
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
        unit = Unit(unit)
        if unit.is_equivalent(fwl.unit,units.spectral()):
            fwl = fwl.to(unit,equivalencies=units.spectral())

    return fwl


def _mag2fluxdensity(mag,band):
    """
    Converts given magnitude to flux density

    Flux density comes out in 'Jansky' units.
    'filter' is one of Sloan's {ugriz}.
    """
    from astropy import units
    from numpy import log,sinh
    mag = mag * units.mag
    logging.debug("Magnitude: {!s}".format(mag))
    b = _softening(band)
    logging.debug("Softening for {}-band: {!s}".format(band,b))
    _beta = (-2.5 / log(10)) * units.mag
    logging.debug("Scale factor (beta): {!s}".format(_beta))
    _f1 = mag/_beta
    _f2 = log(b)
    _f3 = sinh( _f1.value - _f2.value )
    f_f0 = 2 * b * _f3
    logging.debug("Flux density in SDSS'system: {!s}".format(f_f0))
    zp_AB = 3631 * units.Jy
    s = zp_AB * f_f0
    logging.debug("Flux density in AB system: {!s}".format(s))
    return s

def _softening(band):
    """
    Returns Sloan's "asinh" magnitude "b" softening parameter
    """
    from astropy import units
    assert band in filters, "Band {} not in {}".format(band,filters)
    _zp = filters[band].get('zeropoint')
    assert 'b' in _zp
    _b = _zp['b'] * units.one
    return _b
