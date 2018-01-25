"""
Specific definition for UKIDSS data

Things like magnitude-to-flux converstion or filters central wavelength
are meant to be here defined.

Sources:
--------
* flux-convertions : http://asd.gsfc.nasa.gov/archive/galex/FAQ/counts_background.html
* FAQ-130 : http://www.galex.caltech.edu/researcher/faq.html#ANSWER130
* vo-filters : http://svo2.cab.inta-csic.es/svo/theory/fps3/index.php?mode=browse&gname=GALEX
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
        unit = units.Unit(unit)
        if unit.is_equivalent(fwl.unit,units.spectral()):
            fwl = fwl.to(unit,equivalencies=units.spectral())

    return fwl

def _mag2fluxdensity(mag,band,unit='Jy'):
    """
    Converts given magnitude to flux density

    Flux density comes out in 'Jansky' units.
    'filter' is one of UKIRT's {YJHK}.
    """
    from astropy import units
    _mag = -mag/2.5
    f0 = _zeropoint(band)
    _w = wavelength(band,'angstrom')
    f = (f0 * 10**_mag) * (_w/_w.to('Hz',units.spectral()))
    return f.to(unit)

def _zeropoint(band):
    """
    Returns Sloan's "asinh" magnitude "b" softening parameter
    """
    from astropy.units import Unit
    # import math as m
    assert band in filters
    _zp = filters[band].get('zeropoint')
    assert 'flux' in _zp
    assert 'mag' in _zp
    _f = _zp['flux'] * Unit(_zp['unit'])
    _m0 = _zp['mag'] / 2.5
    # _f = _f * m.pow(10,_m0)
    _f = _f * 10**_m0
    return _f



# from astropy import units
# from astropy.units import Unit
#
# class Filter:
#     def __init__(self,column_filters):
#         '''
#         'column_filters' link catalog's columns to instrument's filters
#         '''
#         self._maps = column_filters
#
#     @property
#     def columns(self):
#         return self._maps
#
#     """
#     'band' is the name of the filter: FUV, NUV
#     """
#     @staticmethod
#     def wavelength(band='full',loc='eff',unit=None):
#         """
#         Returns filter's wavelength according to 'loc' requested
#
#         'loc' can be 'min','max' or 'eff', meaning the "minimum",
#         "maximum", or "effective" filter wavelength values.
#         'central' is accepted as synonym for 'effective'.
#         Wavelengths are returned as `~astropy.units.Unit`.
#         """
#         assert band in filters
#         # band = band.upper()
#         _w = filters[band].get('wavelength')
#         assert loc in _w
#         _v = _w.get(loc) * Unit(_w[Unit])
#         if unit is not None:
#             if Unit(unit).is_equivalent(_v.unit,units.spectral()):
#                 _vv = _v.to(unit,equivalencies=units.spectral())
#                 _v = _vv
#         return _v
#
#     @staticmethod
#     def zeropoint(band):
#         """
#         Returns Sloan's "asinh" magnitude "b" softening parameter
#         """
#         import math as m
#         assert band in filters
#         _zp = filters[band].get('zeropoint')
#         assert 'flux' in _zp
#         assert 'mag' in _zp
#         _f = _zp['flux'] * Unit(_zp[Unit])
#         _m0 = _zp['mag'] / 2.5
#         _f = _f * m.pow(10,_m0)
#         return _f
#
#     @staticmethod
#     def mag2fluxdensity(mag,band):
#         """
#         Converts given magnitude to flux density
#
#         Flux density comes out in 'Jansky' units.
#         'filter' is one of UKIRT's {YJHK}.
#         """
#         from numpy import power
#         _mag = -mag/2.5
#         f0 = Filter.zeropoint(band)
#         f = f0 * power(10,_mag)
#         f = f * Unit('angstrom/Hz')
#         return f.to('Jy')
#
#     @staticmethod
#     def fluxdensity2flux(flux,band):
#         from astropy.units import spectral
#         freq = Filter.wavelength(band).to('Hz',spectral())
#         flux = flux.to('mW m-2 Hz-1')
#         f_flux = flux * freq
#         return f_flux
#
#     @staticmethod
#     def mag2flux(mag,band):
#         flux = Filter.mag2fluxdensity(mag,band).to('mW m-2 Hz-1')
#         f_flux = Filter.fluxdensity2flux(flux,band)
#         return f_flux
#
#     @staticmethod
#     def flux(mag,band):
#         return Filter.mag2flux(mag,band)
