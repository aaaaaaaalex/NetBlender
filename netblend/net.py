
import bpy

"""
Custom Blender object
"""
class Net:


    """
    'centeroffset1D' takes the length of a layer and returns a starting offset
        such that the layer will be centered with the net's largest layer.
    layer_length <int>: the size of the layer to center
    axis <int>: the index of the axis to center the point on - x: 0, y: 1, z: 2
    """
    def __centeroffset1D__(self, layer_length, axis=1):
        pass


    """
    'centeroffset2D' takes a layer's dimensions and returns a starting offset
        such that the layer will be centered with the net's largest layer.
    layer_dimen <tuple[2]>: the y and z dimensions (assuming the x-dimension is 1) of the layer to center
    """
    def __centeroffset2D__(self, layer_dimen):
        pass


    """
    'make' adds neuron objects to the scene according to the network shape
    origin <tuple[3]>: coordinates to begin building from
    meshfunc <func>: the primitive mesh function to call for each neuron
    centered <bool>: center layers relative to one-another
    """
    def make(self, origin=(0,0,0), meshfunc=bpy.ops.mesh.primitive_cube_add, centered=False):
        self.neurons = []

        next_neuron_loc = [0,0,0]
        # construct the network one layer at a time
        for layer in self.arch:
            # is the layer 1-d or 2-d
            if type(layer) is int:
                for neuron in range(layer):
                    # create and collect references to new neuron objects
                    meshfunc( radius=self.neuron_radius, location=tuple(next_neuron_loc) )
                    self.neurons.append(bpy.context.active_object)

                    # offset origin by the scale for every iteration
                    next_neuron_loc[1] += self.scale[1]

            elif type(layer) is list:
                assert type(layer[0]) is int, "Bad layer shape: A 2-d layer must have shape [x, y]"

                # make a grid for 2-d layers
                for y in range(layer[0]):
                    for z in range(layer[1]):
                        meshfunc( radius=self.neuron_radius, location=tuple(next_neuron_loc) )
                        self.neurons.append(bpy.context.active_object)
                        next_neuron_loc[2] += self.scale[2]
                    next_neuron_loc[1] += self.scale[1]
                    next_neuron_loc[2] = origin[2]

            next_neuron_loc[0] += self.scale[0]
            next_neuron_loc[1] = origin[1]

        return self.neurons


    """
    Construct a full neural net blender object. Each neuron is a primitive object.
    config <dict>: should contain 'arch' and 'activations_sequence' lists
    """
    def __init__ (self, config):
        self.neuron_radius = 0.015
        self.scale = (.75, 0.05, 0.05)
        self.arch = config['arch']
        self.activations_sequence = config['activations']
