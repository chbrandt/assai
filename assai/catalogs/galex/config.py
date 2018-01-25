
VO = {

    "url"     : "http://gsss.stsci.edu/webservices/vo/ConeSearch.aspx?CAT=GALEX&",

    "columns" : "IAUname,RA,DEC,fuv_mag,nuv_mag".split(','),

    "phot" : {
      'fuv_mag' : 'FUV',
      'nuv_mag' : 'NUV'
    },

    "pos" : {
      'ra' : 'RA',
      'dec': 'DEC'
    },

    "waveband" : "uv"
}
