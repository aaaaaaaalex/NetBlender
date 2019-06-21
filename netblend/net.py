import bpy

"""
Custom Blender object
"""
class Net:

    """
    'centeroffset1D' takes the y-axis length of a layer and returns a starting offset
        such that the layer will be centered relative to the net's widest layer.
    layer_length <int>: the size (width) of the layer being centered
    axis <int>: index of axis to center on - x:0 (not supported), y:1, z:2
    """
    def __centeroffset1D__(self, layer_length, axis=1):
        assert axis != 0 and axis < 3, "Invalid axis of {} passed.\n\tA layer can only be centered according to the y-axis(1) or z-axis(2)".format(axis)
        largest_layer = self.__widest_layer__ if axis == 1 else self.__tallest_layer__

        # calculate the scaled lengths of the layers
        scaled_subject_layer = layer_length  * self.scale[axis]
        scaled_largest_layer = largest_layer * self.scale[axis]

        layer_padding = scaled_largest_layer - scaled_subject_layer
        padding_start = layer_padding / 2

        return padding_start


    """
    'centeroffset2D' takes a layer's dimensions and returns a 2-d starting offset
        such that the layer will be centered with the net's largest layer.
    layer_dimensions <tuple[2]>: the y and z dimensions (assuming the x-dimension is 1) of the layer to center
    """
    def __centeroffset2D__(self, layer_dimensions):
        assert type(layer_dimensions) is tuple and len(layer_dimensions) == 2, "Invalid layer dimensions: arg must be a tuple with two items representing the layer's y and z dimensions"
        y_offset = self.__centeroffset1D__(layer_dimensions[0], axis=1)
        z_offset = self.__centeroffset1D__(layer_dimensions[1], axis=2)

        return (y_offset, z_offset)


    """
    'make' adds neuron objects to the scene according to the network's shape
    origin <tuple[3]>: coordinates to begin building from
    meshfunc <func>: the primitive mesh function to call for each neuron
    centered <bool>: center layers relative to one-another
    """
    def make(self, origin=(0,0,0), meshfunc=bpy.ops.mesh.primitive_cube_add, centered=True):
        self.neurons = []

        next_neuron_loc = [0,0,0]
        # construct the network one layer at a time
        for layer in self.arch:

            assert type(layer[0]) is int, "Bad layer shape: A 2-d layer must have shape [y-axis-size, z-axis-size]"

            if centered:
                # list-type layers are expected to be 2-d, but handle for 1-d lists
                try:
                    y_z_dimensions = (layer[0], layer[1])
                except IndexError:
                    z_z_dimensions = (layer[0], 1)

                offsetY, offsetZ = self.__centeroffset2D__(y_z_dimensions)
                next_neuron_loc[1] += offsetY
            else:
                offsetY = 0
                offsetZ = 0

            # make a grid for 2-d layers
            for y in range(layer[0]):
                # offset each column of neurons on the z-axis if necessary
                next_neuron_loc[2] = origin[2] + offsetZ

                for z in range(layer[1]):
                    meshfunc( radius=self.neuron_radius, location=tuple(next_neuron_loc) )
                    self.neurons.append(bpy.context.active_object)
                    next_neuron_loc[2] += self.scale[2]

                # advance to the next column starting point
                next_neuron_loc[1] += self.scale[1]

            # advance the next neuron location on x-axis and reset it on the y-axis
            next_neuron_loc[0] += self.scale[0]
            next_neuron_loc[1] = origin[1]

        return self.neurons


    """
    Construct a full neural net blender object. Each neuron is a primitive object.
    config <dict>: should contain 'arch' and 'activations_sequence' lists
    """
    def __init__ (self, config):
        self.neuron_radius = 0.015
        self.scale = (.5, 0.05, 0.05)

        self.arch = []
        self.activations_sequence = config['activations']

        self.__tallest_layer__ = None
        self.__widest_layer__ = None

        # get largest layer in arch
        widest = 0
        tallest = 0
        for lyr in config['arch']:
            assert (type(lyr) is int or type(lyr) is list), "A layer can only be of type 'int' or 'list'.\n\tlayer: {}\n\ttype: {}".format(lyr, type(lyr))
            if type(lyr) is int:
                lyrwidth = lyr
                lyrheight = 1
                lyr = [lyrwidth, lyrheight]

            # layers of type list are expected to have a y-size and z-size, but allow single-dimension lists also
            else:
                assert len(lyr) <= 2, "A layer cannot have more than 2 dimensions.\n\tlayer: {}\n\tlength:{}".format(lyr, len(lyr))

                lyrwidth = lyr[0]
                if len(lyr) > 1: lyrheight = lyr[1]
                else: lyrheight = 1

            if lyrwidth > widest: widest = lyrwidth
            if lyrheight > tallest: tallest = lyrheight
            self.arch.append(lyr)

        self.__widest_layer__ = widest
        self.__tallest_layer__ = tallest

        return
