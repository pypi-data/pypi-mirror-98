from typing import Tuple
import h5py
import numpy as np
from ..model.bead_states import BeadStates


class HDF5BeadDataReader:

    def __init__(self, fname: str):
        self.h5_file = h5py.File(fname, "r")
        self.data_set_coords = self.h5_file.get("bead_coordinates")
        self.data_set_links = self.h5_file.get("bead_links")
        self.data_set_filaments = self.h5_file.get("filaments")
        self.data_set_steps = self.h5_file.get("steps")
        self.data_set_bead_ids = self.h5_file.get("bead_ids")
        
        if self.h5_file.attrs["FORMAT"] == "AFINES":
            self.afines_format = True
        else:
            self.afines_format = False

    def get_system_state_at_time_step(
            self, time_step: int) -> Tuple[np.ndarray, BeadStates]:

        coords_array = self.data_set_coords[time_step, :, :].flatten()
        links_array = self.data_set_links[time_step, :, :].flatten()
        bead_states = BeadStates(links_array)
        return coords_array, bead_states    
