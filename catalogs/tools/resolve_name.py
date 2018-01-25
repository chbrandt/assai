from __future__ import print_function
import astropy

def resolve_name(name):
    """
    Return ICRS Coordinates from given object 'name'

    Input:
     - name : str
        Object designation/name
    Output:
     - icrs : ~astropy.coordinates.SkyCoord
        Object with 'ra' and 'dec' attributes
    """
    from astropy.coordinates import get_icrs_coordinates as get_coords
    try:
        coords = get_coords(name)
    except:
        coords = None
    return coords

def name2coords(name):
    """
    Return RA,Dec coordinates for given object Name

    Input:
     - name : str
        Object designation/name
    Output:
     - position : (float,float)
        Tuple with (RA,Dec) coordinates in degree
    """
    icrs = resolve_name(name)
    pos = (icrs.ra.value,icrs.dec.value) if icrs else None
    return pos


if __name__ == '__main__':
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description='Resolve object name to (ra,dec) coordinates'
    )

    parser.add_argument("object", type=str,
                        help="Object name. Ex: 3c279")

    args = parser.parse_args()
    obj = args.object

    pos = name2coords(obj)
    if pos is None:
        print("\nERROR: Object '{}' not resolved.\n".format(obj),file=sys.stderr)
        sys.exit(1)

    ra,dec = pos
    print("{:9s} {:9s}".format('ra','dec'))
    print("{:3.5f} {:3.5f}".format(ra,dec))
    sys.exit(0)
