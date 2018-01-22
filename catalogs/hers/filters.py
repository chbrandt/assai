"""
The HerS catalog

Filter information from the SVO filters service:
* http://svo2.cab.inta-csic.es/svo/theory/fps/index.php?id=Herschel/SPIRE.PLW&&mode=browse&gname=Herschel&gname2=SPIRE
"""

import logging
import json
import os
_here = os.path.dirname(__file__)

filters = os.path.join(_here, 'filters.json')
with open(filters, 'r') as f:
    filters = json.load(f)


def flux_density(flxd, band=None, unit=None):
    if unit:
        flxd = flxd.to(unit)
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
