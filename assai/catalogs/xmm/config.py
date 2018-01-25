
VO = {

    "url"     : "https://heasarc.gsfc.nasa.gov/cgi-bin/vo/cone/coneGet.pl?table=xmmssc&",

    "columns" : "name,ra,dec,ep_8_flux,ep_1_flux,ep_2_flux,ep_3_flux,ep_4_flux,ep_5_flux".split(','),

    "phot" : {
        "ep_8_flux" : "8_b",
        "ep_1_flux" : "1_b",
        "ep_2_flux" : "2_b",
        "ep_3_flux" : "3_b",
        "ep_4_flux" : "4_b",
        "ep_5_flux" : "5_b"
    },
    'pos': {
        'ra': 'ra',
        'dec': 'dec'
    },
    'waveband': 'x-ray'
}
