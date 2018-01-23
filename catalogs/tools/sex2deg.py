from __future__ import print_function
import astropy

def sex2deg(sex):
    """
    Return coordinates in (ICRS) degrees
    """
    from astropy.coordinates import SkyCoord
    try:
        coords = SkyCoord(sex, unit=('hourangle', 'deg'))
    except:
        return None
    return coords.ra.value,coords.dec.value


if __name__ == '__main__':
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description='Transform sexagesimal coordinates to degrees'
    )

    parser.add_argument("coords", type=str,
                        help="Coordinates in 'hh:mm:ss,dd:mm:ss'.")

    args = parser.parse_args()

    sex = args.coords
    deg = sex2deg(sex)
    if deg is None:
        print("\nERROR: Coordinates '{}' not understood.\n".format(sex),file=sys.stderr)
        sys.exit(1)

    ra,dec = deg
    print("{:9s} {:9s}".format('ra','dec'))
    print("{:3.5f} {:3.5f}".format(ra,dec))
    sys.exit(0)
