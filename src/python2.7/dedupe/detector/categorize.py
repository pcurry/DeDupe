#!/usr/bin/env python2.7

import os
import os.path

# Project local imports
import dedupe.util.helper_functions as helper_functions



class GenericCategorizer(object):
    """ Generic categorizer, 

    """

    def __init__(self):
        self.results = {}
        
