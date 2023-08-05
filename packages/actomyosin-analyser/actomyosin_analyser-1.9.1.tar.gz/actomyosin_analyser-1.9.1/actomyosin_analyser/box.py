

class Box:

    def __init__(self):
        self.box_sizes = None

    def get_parameters_from_config_reader(self, config_reader):
        self.box_sizes = config_reader.get_box_sizes()

    def get_distance_vector_periodic_boundary(self, r1, r2):
        """
        r1 and r2 need to be numpy.ndarrays of shape (3,).
        """
        d = r2 - r1
        for i in range(3):
            d_i = d[i]
            size_i = self.box_sizes[i]
            half_size = size_i / 2
            if d_i > half_size:
                d[i] = d[i] - size_i
            elif d_i < -half_size:
                d[i] = d[i] + size_i
        return d
