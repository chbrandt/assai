
VO = {

    "url"     : "http://skyserver.sdss.org/vo/ConeSearch/sdssConeSearch.asmx/ConeSearch?",

    "columns" : "OBJID,RA,DEC,U,G,R,I,Z".split(','),

    "phot" : {
      'U' : 'u',
      'G' : 'g',
      'R' : 'r',
      'I' : 'i',
      'Z' : 'z'
    },

    "pos" : {
      'ra' : 'RA',
      'dec': 'DEC'
    },

    "waveband" : "optical"
}
