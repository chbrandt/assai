from astropy.units import Unit

def init_unit(unit):
    from astropy import units as u
    if isinstance(unit,Unit):
        # nothing to do
        return unit
    if unit is None:
        # undefined unit
        return u.one
    if isinstance(unit,str):
        if not unit.strip():
            # undefined unit
            return u.one
    return u.Unit(unit,parse_strict='warn')

def are_equivalent(unit1,unit2,equivalencies=None):
    _u1 = get_unit(unit1)
    _u2 = get_unit(unit2)
    return _u1.is_equivalent(_u2,equivalencies=equivalencies)

def is_dimensionless(unit):
    _u = get_unit(unit)
    return _u.is_equivalent(1)

def can_convert(old_unit,new_unit):
    if is_dimensionless(old_unit):
        return True
    return are_equivalent(old_unit,new_unit)

def convert(data,old_unit,new_unit):
    if not len(data):
        return None
    if not are_equivalent(old_unit,new_unit):
        return None
    _uo = get_unit(old_unit)
    _un = get_unit(new_unit)
    _do = data * _uo
    _dn = _do.to(_un)
    return _dn
