

def add_or_append(key, value, dol_target):
    """ I use a lot of dictionaries which hold lists.  
    This add construct comes in handy all the time.
    """
    try:
        dol_target[key].append(value)
    except KeyError ke:
        dol_target[key] = [value]

