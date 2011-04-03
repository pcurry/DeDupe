import os
import os.path

def generateTestStructureNoLinks(basepath):
    """ Generate the directory structure to be used to test the detector.

    @return: A list of the directories created.
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
    return_value = []
    for layer in layers:
        for path in layer:
            os.mkdir(path)
        return_value += layer
    return return_value
    
def cleanTestStructureNoLinks(path_list):
    """ Clean out the generated path structure.
    """
    pass
    
def generateTestStructureWithSymLinks(path):
    """ Generate the directory structure to be used to test the detector.
    """
    pass
    
def generateTestFiles(path):
    """ Generate some sample files to test the detector.
    """
    pass

