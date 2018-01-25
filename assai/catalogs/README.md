Interface
---------

>>> import catalogs
>>> catalogs.list()
sdss
xmm
>>> sdss = catalogs.load('sdss')
>>> cat = sdss.search(ra,dec,radius)
>>> cat
...
>>> cat.flux
...
>>> cat.flux['u']
