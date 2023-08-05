import numpy as np


class FilamentIndexer(object):

    def __init__(self, filament_id):
        self.filament_id = filament_id
        self._dict_time_index_to_indices = {}
        self.t_index_creation = None
        self.t_index_termination = None
        
    def set_indices_at_t_index(self, t_index: int, index_array: np.ndarray):
        self._dict_time_index_to_indices[t_index] = index_array
        if len(index_array) == 0:                        
            if self.t_index_creation is None:
                return
            elif self.t_index_termination is None:
                self.t_index_termination = t_index
            return
        if self.t_index_creation is None:
            self.t_index_creation = t_index

    def get_indices_at_t_index(self, t_index: int) -> np.ndarray:
        return self._dict_time_index_to_indices[t_index]

    def __getitem__(self, t_index: int) -> np.ndarray:
        return self._dict_time_index_to_indices[t_index]

    def __setitem__(self, t_index: int, index_array: np.ndarray):
        if not isinstance(t_index, int):
            object.__setattr__(self, t_index, index_array)
            return
        self.set_indices_at_t_index(t_index, index_array)

    def __str__(self):
        line = "{}: {},"
        s = "{"
        t_indices = list(self._dict_time_index_to_indices.keys())
        t_indices.sort()
        
        for t_index in t_indices[:3]:
            s += line.format(t_index, self._dict_time_index_to_indices[t_index])
            s += "\n"
        if len(t_indices) > 6:
            s += "...\n"
        for t_index in t_indices[-3:]:
            s += line.format(t_index, self._dict_time_index_to_indices[t_index])
            s += "\n"
        s = s[:-2]
        s += "}"
        return s

    def __repr__(self):
        return self.__str__()
