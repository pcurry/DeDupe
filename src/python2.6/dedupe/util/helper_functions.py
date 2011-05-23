import os.path

def add_or_append(key, value, dict_of_lists):
    """ I use a lot of dictionaries which hold lists.  
    This add construct comes in handy all the time.
    """
    try:
        dict_of_lists[key].append(value)
    except KeyError as ke:
        dict_of_lists[key] = [value]


def is_symlink_dir(fqn):
    """ Expects fqn to be a fully-qualified filename.  
    Returns true if the fqn both is a symlink, and points to a directory.
    """
    return os.path.islink(fqn) and os.path.isdir(fqn)

def is_unvisited_symlink_dir(fqn, visited):
    """ Expects a fully-qualified filename, and a dictionary of paths that
    are directories.
    Returns true if the fqn is a symlink and a dir, and not present in visited.
    """
    link_not_visited = fqn not in visited
    target_not_visited = os.path.realpath(fqn) not in visited
    return is_symlink_dir(fqn) and link_not_visited and target_not_visited 
    
def process_extension(filename):
    pass
