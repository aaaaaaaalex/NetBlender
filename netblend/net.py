import bpy

"""
Custom Blender object
"""
class Net:

    """
    'centeroffset1D' takes the y-axis length of a layer and returns a starting offset
        such that the layer will be centered relative to the net's widest layer.
    layer_length <int>: the size (width) of the layer being centered
    """
    def __centeroffset1D__(self, layer_length):
        # get largest layer in arch if it hasnt already been cached
        if not self.__widest_layer__:
            highest = 0
            for lyr in self.arch:
                if type(lyr) is int: lyrwidth = lyr
                elif type(lyr) is list: lyrwidth = lyr[0]
                if lyrwidth > highest: highest = lyrwidth

            self.__widest_layer__ = highest

        # calculate the scaled lengths of the layers
        scaled_next_layer = layer_length * self.scale[1]
        scaled_largest_layer = self.__widest_layer__ * self.scale[1]

        layer_padding = scaled_largest_layer - scaled_next_layer
        padding_start = layer_padding/2

        return padding_start


    """
    'centeroffset2D' takes a layer's dimensions and returns a 2-d starting offset
        such that the layer will be centered with the net's largest layer.
    layer_dimen <tuple[2]>: the y and z dimensions (assuming the x-dimension is 1) of the layer to center
    """
    def __centeroffset2D__(self, layer_dimen):


        return (0,0)


    """
    'make' adds neuron objects to the scene according to the network's shape
    origin <tuple[3]>: coordinates to begin building from
    meshfunc <func>: the primitive mesh function to call for each neuron
    centered <bool>: center layers relative to one-another
    """
    def make(self, origin=(0,0,0), meshfunc=bpy.ops.mesh.primitive_cube_add, centered=False):
        self.neurons = []

        next_neuron_loc = [0,0,0]
        # construct the network one layer at a time
        for layer in self.arch:

            # if the layer is 1-d
            if type(layer) is int:
                #offset the starting location is centering is required
                if centered: next_neuron_loc[1] += self.__centeroffset1D__(layer)
                for neuron in range(layer):
                    # create and collect references to new neuron objects
                    meshfunc( radius=self.neuron_radius, location=tuple(next_neuron_loc) )
                    self.neurons.append(bpy.context.active_object)

                    # offset origin by the scale for every iteration
                    next_neuron_loc[1] += self.scale[1]

            # if the layer is 2-d
            elif type(layer) is list:
                assert type(layer[0]) is int, "Bad layer shape: A 2-d layer must have shape [x, y]"
                if centered:
                    offsetY, offsetZ = self.__centeroffset2D__(layer)
                    next_neuron_loc[1] += offsetY
                    next_neuron_loc[2] += offsetZ

                # make a grid for 2-d layers
                for y in range(layer[0]):
                    for z in range(layer[1]):
                        meshfunc( radius=self.neuron_radius, location=tuple(next_neuron_loc) )
                        self.neurons.append(bpy.context.active_object)
                        next_neuron_loc[2] += self.scale[2]
                    next_neuron_loc[1] += self.scale[1]
                    if centered is False: next_neuron_loc[2] = origin[2]

            # advance the next neuron location on x-axis and reset it on the y-axis
            next_neuron_loc[0] += self.scale[0]
            next_neuron_loc[1] = origin[1]

        return self.neurons


    """
    Construct a full neural net blender object. Each neuron is a primitive object.
    config <dict>: should contain 'arch' and 'activations_sequence' lists
    """
    def __init__ (self, config):
        self.__uidest_layer__ = None
        self.neuron_radius = 0.015
        self.scale = (.75, 0.05, 0.05)
        self.arch = config['arch']
        self.activations_sequence = config['activations']
