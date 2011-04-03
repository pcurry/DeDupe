import os
import os.path

def generateTestStructureNoLinks(basepath):
    """ Generate the directory structure to be used to test the detector.

    @return: A list of lists, each list being a layer of the directories created.
    """
    # Generate the paths, then create the directories.
    dirname_format = "test-layer%d-dir%d"
    per_layer = layer_depth = 4  # Testing directory structure size parameters
    layers = [[basepath]] # Start with the base path
    for i in range(1, layer_depth + 1):
        this_layer = []
        for path in layers[i-1]:
            this_layer += [ os.path.join(path, dirname_format % (i,j))
                            for j in range(per_layer) ]
        layers.append(this_layer)
    layers = layers[1:]
    # FIXME: Think about doing this using os.makepaths() and just the leaves.
    for layer in layers:
        for path in layer:
            os.mkdir(path)
    return layers
    
def cleanTestStructureNoLinks(path_list):
    """ Clean out the generated path structure.
    """
    # shutil.rmtree() might be useful for this.
    pass
    
def generateTestStructureWithSymLinks(basepath):
    """ Generate the directory structure to be used to test the detector.
    """
    # Generate a no-link structure, then put in some links
    pass 
    
def generateTestFiles(path):
    """ Generate some sample files to test the detector.
    """
    pass

