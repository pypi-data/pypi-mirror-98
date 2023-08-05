import os
from configparser import ConfigParser
import numpy as np
import h5py

from typing import Tuple, Dict

from afines_reader.actins_reader import ActinsReader
from afines_reader.motors_reader import MotorsReader
from afines_reader.model.actins import Actins
from afines_reader.model.motors import Motors

class AfinesConverter:

    def __init__(self, afines_output_dir):
        self.afines_dir = os.path.abspath(afines_output_dir)

        self.actins_reader = ActinsReader(self.afines_dir + "/txt_stack/actins.txt")
        self.pmotors_reader = MotorsReader(self.afines_dir + "/txt_stack/pmotors.txt")
        self.amotors_reader = MotorsReader(self.afines_dir + "/txt_stack/amotors.txt")

        self.actins_reader.read()
        self.pmotors_reader.read()
        self.amotors_reader.read()

        self.h5_file = None
        self.config = ConfigParser()

    def convert(self, fname_h5: str):        
        self.h5_file = h5py.File(fname_h5)

        self.h5_file.attrs['FORMAT'] = "AFINES"
        config_content = open(self.afines_dir + "/data/config_full.cfg", 'rt').read()
        self.h5_file.attrs['CONFIG'] = config_content
        # insert dummy section header, otherwise can't use ConfigParser
        self.config.read_string("[DUMMY]\n" + config_content)
        
        bead_array, link_array, filament_array = self._convert_actins_to_arrays()
        self.h5_file["bead_coordinates"] = bead_array
        self.h5_file["bead_links"] = link_array
        self.h5_file["filaments"] = filament_array

        bead_ids = self._create_full_bead_ids_array(bead_array.shape[0], bead_array.shape[1])
        self.h5_file["bead_ids"] = bead_ids

        xlink_coords, xlink_links = self._convert_motors_to_arrays(self.pmotors_reader.motors)
        self.h5_file["crosslink_coordinates"] = xlink_coords
        self.h5_file["crosslink_links"] = xlink_links

        motor_coords, motor_links = self._convert_motors_to_arrays(self.amotors_reader.motors)
        self.h5_file["motor_coordinates"] = motor_coords
        self.h5_file["motor_links"] = motor_links

        time_steps = self._convert_t_array_to_steps()
        self.h5_file["steps"] = time_steps
                
        self.h5_file.close()

    def _create_full_bead_ids_array(self, n_time_steps, n_beads):
        return np.mgrid[:n_time_steps, :n_beads][1].astype(np.int32)
        
    def _convert_t_array_to_steps(self) -> np.ndarray:
        t_actins  = np.array(sorted(self.actins_reader.actins.keys()))
        t_amotors = np.array(sorted(self.amotors_reader.motors.keys()))
        t_pmotors = np.array(sorted(self.pmotors_reader.motors.keys()))

        try:
            assert (t_actins  == t_amotors).all()
            assert (t_actins  == t_pmotors).all()
            assert (t_amotors == t_pmotors).all()
        except AssertionError as error:
            msg = "Time points read from actins.txt, amotors.txt and pmotors.txt do not all match!"
            raise RuntimeError(msg)

        dt = float(self.config["DUMMY"]["dt"])
        
        t = t_actins
        t_as_steps = np.around(t / dt).astype(np.int)
        return t_as_steps        
        
    def _convert_motors_to_arrays(
            self, motors_dict: Dict[float, Motors]) -> Tuple[np.ndarray, np.ndarray]:
        actins_dict = self.actins_reader.actins
        N_max = self._determine_N_max_motors(motors_dict)        
        coords_array = np.full((len(motors_dict.keys()), N_max, 4), np.nan)
        links_array  = np.full((len(motors_dict.keys()), N_max, 2), -1, dtype=np.int32)
        for i, ti in enumerate(sorted(motors_dict.keys())):
            motors = motors_dict[ti]
            actins = actins_dict[ti]
            coords_array[i, :len(motors.x), 0] = motors.x
            coords_array[i, :len(motors.x), 1] = motors.y
            coords_array[i, :len(motors.x), 2] = motors.dx
            coords_array[i, :len(motors.x), 3] = motors.dy
            links_array[i, :len(motors.x), 0] = self._get_bead_index_from_fidx_and_lidx(
                motors.fidx0, motors.lidx0, actins)
            links_array[i, :len(motors.x), 1] = self._get_bead_index_from_fidx_and_lidx(
                motors.fidx1, motors.lidx1, actins)
        return coords_array, links_array

    def _get_bead_index_from_fidx_and_lidx(
            self, fidx: np.ndarray, lidx: np.ndarray, actins: Actins) -> np.ndarray:
        bead_idx = np.empty_like(fidx, dtype=np.int32)
        for i in range(len(fidx)):        
            fidx_i = fidx[i]
            if fidx_i == -1 or lidx[i] == -1:
                bead_idx[i] = -1
                continue
            beads_with_fidx = np.where(actins.fidx == fidx_i)[0]
            bead_idx[i] = beads_with_fidx[lidx[i]]
        return bead_idx

    def _determine_N_max_motors(self, motors_dict: Dict[float, Motors]) -> int:
        N_max = 0
        for ti in motors_dict:
            motors = motors_dict[ti]
            N = len(motors.x)
            if N > N_max:
                N_max = N
        return N_max

    def _convert_actins_to_arrays(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:        
        actins_dict = self.actins_reader.actins
        N_max_beads, N_max_filaments = self._determine_N_max_beads_and_filaments(actins_dict)
        bead_array = np.full((len(actins_dict.keys()), N_max_beads, 2), np.nan)
        link_array = np.full((len(actins_dict.keys()), N_max_beads, 2), -1, dtype=np.int32)
        filament_array = np.full((len(actins_dict.keys()), N_max_filaments, 3), -1, dtype=np.int32)
        for i, ti in enumerate(sorted(actins_dict.keys())):
            actins = actins_dict[ti]
            if (actins.r != actins.r[0]).any():
                msg = "Radii of beads are not uniform! Need to store that information somewhere."
                raise NotImplementedError(msg)
            bead_array[i, :len(actins.x), 0] = actins.x
            bead_array[i, :len(actins.x), 1] = actins.y
            unique_fidx = np.unique(actins.fidx)
            for j, fidx in enumerate(unique_fidx):
                beads_with_fidx = np.where(actins.fidx == fidx)[0]
                if len(beads_with_fidx) < 2:
                    continue
                assert (beads_with_fidx == np.arange(beads_with_fidx[0], beads_with_fidx[-1] + 1))\
                    .all()
                filament_array[i, j, 0] = fidx
                filament_array[i, j, 1] = beads_with_fidx[0]
                filament_array[i, j, 2] = beads_with_fidx[-1]
                link_array[i, beads_with_fidx[0]: beads_with_fidx[-1], 1] =\
                    beads_with_fidx[0: -1] + 1
                link_array[i, beads_with_fidx[1]: beads_with_fidx[-1] + 1, 0] =\
                    beads_with_fidx[0: -1]
        return bead_array, link_array, filament_array
                
    def _determine_N_max_beads_and_filaments(
            self, actins_dict: Dict[float, Actins]) -> Tuple[int, int]:
        N_max_beads = 0
        N_max_filaments = 0
        for ti in actins_dict:
            actins = actins_dict[ti]
            if len(actins.x) > N_max_beads:
                N_max_beads = len(actins.x)
            N_filaments = len(np.unique(actins.fidx))
            if N_filaments > N_max_filaments:
                N_max_filaments = N_filaments
        return N_max_beads, N_max_filaments
