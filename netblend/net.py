
import bpy

"""
Custom Blender object
"""
class Net:

    """
    'make' adds neuron objects to the scene according to the network shape
    origin: coordinates to begin building from
    meshfunc: the primitive mesh function to call for each neuron
    centered: center the neurons around the x-axis, otherwise, align them to branch off the x-axis
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
    Construct a full neural net blender object.
    Each neuron is a primitive.
    """
    def __init__ (self, config):
        self.neuron_radius = 0.015
        self.scale = (.75, 0.05, 0.05)
        self.arch = config['arch']
        self.activations_sequence = config['activations']
