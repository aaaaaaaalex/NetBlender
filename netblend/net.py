
"""
Custom Blender object
"""
class Net:
    def __init__ (self, config):
        self.arch = config['arch']
        self.activations_sequence = config['activations']
