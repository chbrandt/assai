
VO = {

    "url"     : "https://irsa.ipac.caltech.edu/SCS?table=allwise_p3as_psd",

    "columns" : "designation,ra,dec,w1mpro,w2mpro,w3mpro,w4mpro".split(','),

    "phot" : {
      'w1mpro' : 'W1',
      'w2mpro' : 'W2',
      'w3mpro' : 'W3',
      'w4mpro' : 'W4'
    },

    "pos" : {
      'ra' : 'ra',
      'dec': 'dec'
    },

    "waveband" : "ir"
}
