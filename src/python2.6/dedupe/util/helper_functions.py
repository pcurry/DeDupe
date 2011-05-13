import os.path

def add_or_append(key, value, dol_target):
    """ I use a lot of dictionaries which hold lists.  
    This add construct comes in handy all the time.
    """
    try:
        dol_target[key].append(value)
    except KeyError as ke:
        dol_target[key] = [value]


def is_symlink_dir(fqn):
    return os.path.islink(fqn) and os.path.isdir(fqn)

def is_unvisited_symlink_dir(fqn, visited):
    return is_symlink_dir(fqn) and os.path.realpath(fqn) not in visited
