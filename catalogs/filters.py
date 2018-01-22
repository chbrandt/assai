from astropy import units

class Filter:
    def __init__(self,photo_module):
        '''
        '''
        # self.cols = photo_columns
        self.phot = photo_module

    def __str__(self):
        # import json
        # return json.dumps(self.phot.filters,indent=2)
        return self.phot.__doc__

    def about(self):
        print(self.phot.filters)

    def flux(self,mag,band,unit='erg s-1 cm-2'):
        """
        Compute nufnu (flux-density * frequency)
        """
        from astropy import units
        _wu = units.Unit('Hz')
        _mu = units.Unit(unit)
        unit = _mu / _wu
        flx = self.phot.flux_density(mag,band,unit)
        freq = self.phot.wavelength(band).to(_wu,units.spectral())
        return flx * freq

    def wavelength(self,band,unit):
        return self.phot.wavelength(band).to(unit,units.spectral())


    # @property
    # def columns(self):
    #     self.cols
