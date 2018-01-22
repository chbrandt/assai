VO = {
    'url': 'https://heasarc.gsfc.nasa.gov/cgi-bin/vo/cone/coneGet.pl?table=hers82cat&',
    'columns': 'ra,dec,flux_250_um,flux_350_um,flux_500_um'.split(','),
    'phot': {
        'flux_250_um': '250um',
        'flux_350_um': '350um',
        'flux_500_um': '500um'
    },
    'pos': {
        'ra': 'ra',
        'dec': 'dec'
    },
    'waveband': 'radio'
}
