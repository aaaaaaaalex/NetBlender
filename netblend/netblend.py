
"""
make an object of meshes representing the neural net
"""
def addnetobject (neural_net):
    pass


"""
Load and parse the config file containing the architecture of a model
"""
def loadarchitecture (filename):
    with open(filename, 'rb') as archf:
        arch = [ 784, 300, 300, 10 ]
    return arch


"""
Load and parse the config file containing information about a model's activations.
Each datapoint in this file will represent the activations of all neurons for a given input.
Each datapoint will be mapped to keyframes.
"""
def loadactivationsequence (filename):
    with open(filename, 'rb') as asf:
        activation_sequence = asf.read()
    return activation_sequence


"""
Load a model architecture and it's activation sequence, given the directory containing the relevant files
"""
def load (dirname):
    arch_location = "{}arch.json".format(dirname)
    activations_location = "{}activations.json".format(dirname)
    neural_net = {
        'arch' : loadarchitecture(arch_location),
        'activation_sequence' = loadactivationsequence(activations_location),
        }

    addnetobject(neural_net)
    return
