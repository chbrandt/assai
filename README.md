# ASsAI

We call it the Advanced Spectral Analysis Interface, *assai* -- pronounced as the
brazilian fruit *açaí*, in honour to my supervisor, passionate about it; He has a point.

The tool in its full capabilities is meant to be an interactive
interface to explore photometric
data available through the VO network in the format of a spectral
energy distribution plot.

Nevertheless, the tool also provide the query-only interface for the
user not interested in graphical outputs.


## Run

```bash
$ python assai.py
```

A new file `assai.html` is created and a web browser window/tab should open
rendering it.


## Howto add a resource/catalog

`assai` reads the catalog services defined in `$ASSAI_DATA`, where
each service is defined by a json file or python package.

The json file is the simplest way to insert a VO-SCS service: we
define the source URL, columns of interest and respective wavelength:

```json
{
  "url": "https://vo.service.net/scs.xml?",
  "column_names": ["RA", "Dec", "Flux_a", "Flux_b", "Flag_q"],
  "column_units": ["deg", "deg", "erg s-1 cm-2", "erg s-1 cm-2", ""],

  "wavelength": {
	"Flux_a": "500nm",
	"Flux_b": "5keV"
  }
}
```

-- /.\
