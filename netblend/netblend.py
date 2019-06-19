import json
from .net import Net

"""
Load and parse the config file containing information about a model's activations.
Each datapoint in this file will represent the activations of all neurons for a given input.
Each datapoint will be mapped to keyframes.
"""
def loadactivationsequence (filename):
    with open(filename, 'rb') as asf:
        activation_sequence = json.loads( asf.read() )
    return activation_sequence


"""
Load a model architecture and it's activation sequence, given the directory containing the relevant files
"""
def load (file_path='/home/alex/Documents/NetBlender/netblend/activations3d.json'):
    neural_net = Net( loadactivationsequence(file_path) )
    return neural_net
