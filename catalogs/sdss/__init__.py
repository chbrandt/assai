from . import filters

from . import config

def _search(url,columns):
    def search(ra,dec,radius):
        from eada.vo import conesearch as cs
        return cs.main(ra,dec,radius,url=url,columns=columns)
    return search
search = _search(url=config.VO['url'], columns=config.VO['columns'])

columns_2_filters = config.VO['phot']

columns_2_position = config.VO['pos']

del config
