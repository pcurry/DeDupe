#!/usr/bin/env python

import os
import os.path

# Project local imports
import dedupe.util.helper_functions as helper_functions

NO_EXTENSION = "No extension"

def process_tree(path, extensions, files_by_size):
    """ Given a path, a dictionary of extensions, and a dictionary
    of files identified by size, walks the path, categorizing files.

    FIXME: Currently doesn't chase symbolic links.  Extend to do so, and
    FIXME: not loop forever.
    """

    #FIXME: I want to log the processing somewhere, so that the user doesn't
    #FIXME: think the process has given up or died.

    visited_directories = {}
    for root, subdirs, localfiles in os.walk(path):
        realroot = os.path.realpath(root)
        # Don't bother re-processing if we've visited this subtree already.
        if realroot in visited_directories:
            continue
        # We categorize each file, which os.walk gives us in a list.
        for filename in localfiles:
            # The filenames in localfires are the names in the directory.
            # Since os.walk doesn't change dir from the root path, we need the 
            # fully-qualified name for this to work.
            fqn = os.path.join(root, filename)
            # os.walk doesn't categorize links to non-files as subdirs.
            # Test the fqn to make sure it's actually a file, so the stat call 
            # doesn't fail.
            if os.path.isfile(fqn):
                process_filename(fqn, files_by_size, extensions)
            # Here we attempt to chase symlinks
            elif helper_functions.is_unvisited_symlink_dir(fqn, 
                                                           visited_directories):
                subdirs.append(filename)
        visited_directories[realroot] = { 'subdir_count': len(subdirs), 
                                          'file_count': len(localfiles) }
    # Debugging / status statement.
    # Return a status.  The extension and file_size dictionaries were 
    # modified by the code.
    return visited_directories


def process_filename(fqn, files_by_size, extensions):
    """ Given a fully-qualified filename, a dictionary of filenames keyed by
    size, and a dictionary of file extensions, update the two dictionaries
    with the relevant information about the file.
    """
    filesize = os.stat(fqn).st_size
    helper_functions.add_or_append(filesize, fqn, files_by_size)
    extension = helper_functions.process_extension(fqn)
    if extension is None:
        extension = NO_EXTENSION
    helper_functions.add_or_append(extension, filesize, extensions)
    

# Next steps:
# 1) Determine which extensions we care about, if any.
# 2) Hash the files of the extensions we care about, if there is more than 
#    one of the same size.
# 3) Compare the hashes of files we care about, and complain if the two files 
#    match.  MD5 might actually be too weak to be useful, the collision rate 
#    is high enough that it may be noticeable in the libraries of files under
#    discussion.  It's around 2^21 according to Wikipedia.


if __name__ is "__main__":
    print "I am the detector module."

