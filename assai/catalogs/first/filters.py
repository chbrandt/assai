# -*- coding:utf8 -*-

"""
Specific definition for FIRST data

Things like magnitude-to-flux converstion or filters central wavelength
are meant to be here defined.

Sources:
--------
* obs-status: http://sundog.stsci.edu/first/obsstatus.html#configinfo
* vo-filters : http://svo2.cab.inta-csic.es/svo/theory/fps3/index.php?mode=browse&gname=GALEX
"""

import logging
import json
import os
_here = os.path.dirname(__file__)

filters = os.path.join(_here,'filters.json')
with open(filters,'r') as f:
    filters = json.load(f)


def flux_density(flxd,band=None,unit=None):
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


# from astropy import units
# from astropy.units import Unit
# class Filter:
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
#     def zeropoint(band=None):
#         """
#         Returns Sloan's "asinh" magnitude "b" softening parameter
#         """
#         assert False
#
#     @staticmethod
#     def mag2fluxdensity(mag,band):
#         """
#         Converts given magnitude to flux density
#
#         Flux density comes out in 'Jansky' units.
#         'filter' is one of UKIRT's {YJHK}.
#         """
#         assert False
#
#     @staticmethod
#     def fluxdensity2flux(flux,band='1.4'):
#         from astropy.units import spectral
#         freq = Filter.wavelength(band).to('Hz',spectral())
#         flux = flux #* Unit('mJy')
#         flux = flux.to('mW m-2 Hz-1')
#         f_flux = flux * freq
#         return f_flux
#
#     @staticmethod
#     def mag2flux(mag,band):
#         # 'mag' in reality is the flux density
#         return Filter.fluxdensity2flux(mag,band='1.4')
