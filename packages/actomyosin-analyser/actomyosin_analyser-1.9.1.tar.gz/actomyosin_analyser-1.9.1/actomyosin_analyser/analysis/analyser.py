from typing import Callable, Dict, Any, Iterable, List, Tuple
from warnings import warn
import math
import json
import numpy as np
import numba
import h5py
from actomyosin_analyser.file_io.data_reader import DataReader
from . import geometry
from ..__init__ import _VERSION
from ..model.bead import Filament

Dataset = h5py.Dataset
_FilamentT = Tuple[np.ndarray, np.ndarray]
_FilamentsT = numba.typed.List  # [_FilamentT]


class Analyser:

    def __init__(self, data_reader: DataReader, analysis_file: str):
        self.data_reader = data_reader
        self.analysis_file = h5py.File(analysis_file, 'a')
        self._offset_filaments = None
        self._particle_positions = None

    def _get_analysis_dataset(self,
                              dset_name: str,
                              compute_function: Callable[[], np.ndarray],
                              **keyword_arguments: Dict[str, Any]) -> np.ndarray:
        kwargs_as_json = None
        if keyword_arguments:
            kwargs_as_json = Analyser._keyword_arguments_to_json_string(keyword_arguments)
            dset_name += '_' + kwargs_as_json
        if dset_name in self.analysis_file:
            dset = self.analysis_file[dset_name]
            self._check_version(dset)
            if keyword_arguments:                
                kwargs = json.loads(dset.attrs['parameters'])
                if kwargs != keyword_arguments:
                    msg = "DataSet '{}' has matching name, but loaded parameters are different!"
                    msg = msg.format(dset.name)
                    raise RuntimeError(msg)
            return np.array(dset)
        data = compute_function(**keyword_arguments)
        self.analysis_file[dset_name] = data
        self.analysis_file[dset_name]\
            .attrs['ACTOMYOSIN_ANALYSER_VERSION'] = _VERSION
        if kwargs_as_json is not None:            
            self.analysis_file[dset_name].attrs['parameters'] = kwargs_as_json
        return data

    def _get_nested_analysis_dataset(self, group_name: str,
                                     compute_function: Callable[[], np.ndarray],
                                     **keyword_arguments: Dict[str, Any]) -> np.ndarray:
        if not keyword_arguments:
            msg = "keyword_arguments can not be empty for Analyser._get_nested_analysis_dataset. "
            msg += "If you have no keywords, use Analyser._get_analysis_dataset instead!"
            raise KeyError(msg)
        kwargs_as_json = Analyser._keyword_arguments_to_json_string(keyword_arguments)
        # hasher = hashlib.sha1(kwargs_as_json)
        # h = hasher.hexdigest()
        h = kwargs_as_json

        if group_name in self.analysis_file:
            group = self.analysis_file[group_name]
        else:
            group = self.analysis_file.create_group(group_name)

        if h in group:
            dset = group[h]
            self._check_version(dset)
            kwargs = json.loads(dset.attrs['parameters'])
            for_comparison = keyword_arguments.copy()
            for k in for_comparison.keys():
                value = for_comparison[k]
                if isinstance(value, tuple):
                    for_comparison[k] = 'hashed_tuple_' + str(hash(value))
            if kwargs != for_comparison:
                msg = "DataSet '{}' has matching name, but loaded parameters are different!".format(
                    dset.name)
                raise RuntimeError(msg)
            return np.array(dset)

        data = compute_function(**keyword_arguments)
        group[h] = data
        group[h].attrs['parameters'] = kwargs_as_json
        group[h].attrs['ACTOMYOSIN_ANALYSER_VERSION'] = _VERSION
        return data

    def _get_parameter(self, parameter_name,
                       compute_function: Callable[[], Any]) -> Any:
        attrs = self.analysis_file.attrs
        if parameter_name in attrs:
            return attrs[parameter_name]
        par = compute_function()
        attrs[parameter_name] = par
        return par

    def get_offset_filaments(self) -> int:
        return self._get_parameter('offset_filaments',
                                   self._determine_offset_filaments)
        
    def _determine_offset_filaments(self) -> int:
        if self._offset_filaments is not None:
            return self._offset_filaments
        self._offset_filaments = self.data_reader.get_n_non_filament_particles()
        return self._offset_filaments

    def get_filaments(self, save: bool=False) -> List[List[Filament]]:
        return self._get_filaments_from_analysis_file_or_data_reader(save)

    def get_trajectories_filaments(self, minimum_image: bool=False) -> np.ndarray:
        return self._get_analysis_dataset('trajectories_filaments',
                                          self._get_trajectories_filament,
                                          minimum_image=minimum_image)

    def get_trajectories_non_filament(self, minimum_image=False) -> np.ndarray:
        return self._get_analysis_dataset('trajectories_non_filament',
                                          self._get_trajectories_non_filament,
                                          minimum_image=minimum_image)

    def get_msd_ensemble(self, particle_indices: List[int], skip=0) -> np.ndarray:
        return self._get_nested_analysis_dataset('msd_ensemble', self._compute_msd_ensemble,
                                                 particle_indices=tuple(particle_indices),
                                                 skip=skip)


    def get_msd(self, particle_indices: List[int], non_filament: bool=False, skip=0) -> np.ndarray:
        if non_filament:
            method = self.get_msd_single_particle_non_filament
        else:
            method = self.get_msd_single_particle
        msd0 = method(particle_indices[0], skip)
        msds = np.full((len(particle_indices), msd0.shape[0], msd0.shape[1]), np.nan)
        msds[0] = msd0
        for i in range(1, len(particle_indices)):
            msds[i] = method(particle_indices[i], skip)
        return msds
    
    def get_msd_single_particle(self, particle_index: int, skip: int) -> np.ndarray:
        return self._get_nested_analysis_dataset('msd_filament', self._compute_msd,
                                                 particle_index=particle_index,
                                                 skip=skip)

    def get_msd_single_particle_non_filament(self, particle_index: int, skip: int) -> np.ndarray:
        return self._get_nested_analysis_dataset('msd_non_filament', self._compute_msd_non_filament,
                                                 particle_index=particle_index,
                                                 skip=skip)

    def get_densities(self, particle_types: Iterable[str], n_bins: np.ndarray,
                      ranges: np.ndarray=None, count: bool=False) -> np.ndarray:
        n_bins, range_x, range_y, range_z =\
            self._convert_binning_parameters_to_lists(n_bins, ranges)
        return self._get_nested_analysis_dataset('densities', self._compute_densities,
                                                 particle_types=particle_types,
                                                 range_x=range_x,
                                                 range_y=range_y,
                                                 range_z=range_z,
                                                 n_bins=n_bins,
                                                 count=count)

    def get_densities_gauss_kernel(self, particle_types: List[str],
                                   n_bins: np.ndarray,
                                   ranges: np.ndarray,
                                   sigmas: np.ndarray) -> np.ndarray:
        n_bins, range_x, range_y, range_z =\
            self._convert_binning_parameters_to_lists(n_bins, ranges)
        sigmas = list(sigmas)
        return self._get_nested_analysis_dataset(
            'densities_gauss_kernel',
            self._compute_densities_gauss_kernel,
            particle_types=particle_types,
            range_x=range_x,
            range_y=range_y,
            range_z=range_z,
            n_bins=n_bins,
            sigmas=sigmas
        )

    def get_link_count(self) -> np.ndarray:
        return self._get_analysis_dataset('link_count', self.data_reader.get_motor_count)

    def get_contour_lengths(self) -> np.ndarray:
        return self._get_analysis_dataset('contour_lengths',
                                          self._compute_contour_lenghts)
    
    def get_end_to_end_distances(self, t_frame: int, n_beads: int) -> np.ndarray:
        """
        Get end-to-end distances of filaments with n_beads at frame t_frame.
        """
        return self._get_nested_analysis_dataset('end_to_end_distances',
                                                 self._compute_end_to_end_distances,
                                                 t=t_frame,
                                                 n_beads=n_beads)

    def get_end_to_end_vectors(self) -> np.ndarray:
        """
        Get end-to-end vectors for all filaments at all frames. 
        
        :return: Array with 3 dimensions: (1) time frame (2) filament ID (3) XYZ coordinates.
        """
        return self._get_analysis_dataset('end_to_end_vectors', self._get_end_to_end_vectors)

    def get_time_in_steps(self) -> np.ndarray:
        return self._get_analysis_dataset('time_in_steps', self._get_time_in_steps)

    def get_energies_stretch_and_bend(self) -> np.ndarray:
        """
        Get bending and stretching energy of filaments.
        """
        energies = self._get_analysis_dataset('energies', self._compute_energies_stretch_and_bend)
        return energies

    def _get_time_in_steps(self):
        return self.data_reader.read_time_as_step_indices()
        
    def _get_trajectories_non_filament(self, minimum_image):
        pos = self.data_reader.read_particle_positions(minimum_image)
        offset = self.get_offset_filaments()
        return pos[:, :offset]

    def _get_trajectories_filament(self, minimum_image: bool):
        pos = self.data_reader.read_particle_positions(minimum_image)
        offset = self.get_offset_filaments()
        return pos[:, offset:]
        
    def _convert_binning_parameters_to_lists(self, n_bins, ranges):
        if ranges is None:
            ranges = self.data_reader.read_box_size()
        if isinstance(ranges, np.ndarray):
            range_x = ranges[0].tolist()
            range_y = ranges[1].tolist()
            range_z = ranges[2].tolist()
        else:
            range_x = list(ranges[0])
            range_y = list(ranges[1])
            range_z = list(ranges[2])
        if isinstance(n_bins, np.ndarray):
            n_bins = n_bins.tolist()
        n_bins = list(n_bins)
        return n_bins, range_x, range_y, range_z

    def _compute_msd(self, particle_index: int, skip: int) -> np.ndarray:
        coords = self.get_trajectories_filaments()[skip:, particle_index]
        return Analyser._compute_msd_from_trajectory(coords)

    def _compute_msd_non_filament(self, particle_index: int, skip: int) -> np.ndarray:
        offset = self.get_offset_filaments()
        if particle_index >= offset:
            msg = "Filaments start at particle index {}.".format(offset)
            msg += " Non-filament particles can't have index larger than that."
            msg += " Your requested particle index: {}".format(particle_index)
            raise KeyError(msg)
        traj = self.get_trajectories_non_filament()[skip:, particle_index]
        return Analyser._compute_msd_from_trajectory(traj)

    def _compute_msd_ensemble(self, particle_indices: Tuple[int], skip: int):
        coords = self.get_trajectories_filaments()[skip:, particle_indices]
        return Analyser._compute_msd_from_trajectory(coords)

    @staticmethod
    @numba.njit
    def _compute_msd_from_trajectory(trajectory: np.ndarray) -> np.ndarray:
        lags = np.arange(1, len(trajectory))
        msd = np.empty((len(lags), 3))
        for lag in lags:
            displacements = trajectory[lag:] - trajectory[:-lag]
            squared_summed = np.sum(displacements**2, axis=-1)
            msd[lag-1, 0] = lag
            msd[lag-1, 1] = np.nanmean(squared_summed)
            msd[lag-1, 2] = np.nanvar(squared_summed)
        return msd

    def _compute_densities(self,
                           particle_types: List[str],
                           range_x: List[float],
                           range_y: List[float],
                           range_z: List[float],
                           n_bins: List[int],
                           count: bool) -> np.ndarray:
        wx = (range_x[1] - range_x[0]) / n_bins[0]
        wy = (range_y[1] - range_y[0]) / n_bins[1]
        wz = (range_z[1] - range_z[0]) / n_bins[2]
        V = wx*wy*wz

        positions = self.data_reader.read_particle_positions()
        pmap, ptypes = self.data_reader.read_particle_types()

        shape = (len(positions), n_bins[0], n_bins[1], n_bins[2])
        densities = np.full(shape, np.nan)

        for t in range(positions.shape[0]):
            pos_t = positions[t]
            ptypes_t = ptypes[t]
            mask = np.zeros_like(ptypes_t, dtype=bool)
            for pt in particle_types:
                mask += (ptypes_t == pmap[pt])
            selected_particles = pos_t[mask]
            bin_indices = Analyser._coordinates_to_bin_indices(selected_particles,
                                                               range_x, wx,
                                                               range_y, wy,
                                                               range_z, wz)
            for i in range(shape[1]):
                for j in range(shape[2]):
                    for k in range(shape[3]):   
                        count_ijk = ((bin_indices[:, 0] == i) &
                                 (bin_indices[:, 1] == j) &
                                 (bin_indices[:, 2] == k)).sum()
                        densities[t, i, j, k] = count_ijk
        if count:
            densities = densities.astype(int)
        else:
            densities = densities/V
        
        return densities

    def _compute_densities_gauss_kernel(self,
                                        particle_types: List[str],
                                        range_x: List[float],
                                        range_y: List[float],
                                        range_z: List[float],
                                        n_bins: List[int],
                                        sigmas: List[float]) -> np.ndarray:
        wx = (range_x[1] - range_x[0]) / n_bins[0]
        wy = (range_y[1] - range_y[0]) / n_bins[1]
        wz = (range_z[1] - range_z[0]) / n_bins[2]
        V = wx*wy*wz


        box = self.data_reader.read_box_size()
        box_l = np.array([
            box[1, 0] - box[0,0],
            box[1, 1] - box[0, 1],
            box[1, 2] - box[0, 2]
        ])

        grid_range = (np.array(sigmas)*4 / np.array([wx, wy, wz])).astype(int)

        positions = self.data_reader.read_particle_positions()
        pmap, ptypes = self.data_reader.read_particle_types()

        shape = (len(positions), n_bins[0], n_bins[1], n_bins[2])
        densities = np.full(shape, np.nan)

        for t in range(positions.shape[0]):
            pos_t = positions[t]
            ptypes_t = ptypes[t]
            mask = np.zeros_like(ptypes_t, dtype=bool)
            for pt in particle_types:
                mask += (ptypes_t == pmap[pt])
            selected_particles = pos_t[mask]
            bin_indices = Analyser._coordinates_to_bin_indices(selected_particles,
                                                               range_x, wx,
                                                               range_y, wy,
                                                               range_z, wz)

            for i in range(shape[1]):
                for j in range(shape[2]):
                    for k in range(shape[3]):
                        mask_ijk = self._get_voxel_mask(
                            bin_indices, grid_range, (i, j, k), shape[1:]
                        )
                        pos_voxel = np.array([
                            (i+0.5) * wx + range_x[0],
                            (j+0.5) * wy + range_y[0],
                            (k+0.5) * wz + range_z[0]
                        ])
                        delta_x = geometry.get_minimum_image_vector(
                            selected_particles[mask_ijk] + box_l/2,
                            pos_voxel+box_l/2,
                            box_l
                        )
                        kernel_density_ijk = Analyser._gauss_3D(delta_x, sigmas).sum()
                        densities[t, i, j, k] = kernel_density_ijk
        return densities

    def _compute_end_to_end_distances(self, t: int, n_beads: int) -> np.ndarray:
        coordinates = self.get_trajectories_filaments()[t]
        filaments = self.data_reader.get_filaments(t)
        box = self.data_reader.read_box_size()
        box = np.array([box[1, 0] - box[0, 0],
                        box[1, 1] - box[0, 1],
                        box[1, 2] - box[0, 2]])
    
        e2e = []
        for fil in filaments:
            if len(fil.items) != n_beads:
                continue
            e2e.append(self._compute_e2e_single_filament(coordinates, fil, box))
        return np.array(e2e)

    def _get_end_to_end_vectors(self) -> np.ndarray:
        raise NotImplementedError
        coordinates = self.get_trajectories_filaments()
        filaments = self.data_reader.get_filaments_all()


    def _compute_e2e_single_filament(self, coordinates: np.ndarray, filament, box) -> float:
        offset_filaments = self.get_offset_filaments()
        fcoords = coordinates[np.array(filament.items)+offset_filaments]
        v_segments = geometry.get_minimum_image_vector(fcoords[:-1], fcoords[1:], box)
        e2e = np.sum(v_segments, axis=0)
        return math.sqrt(e2e[0]**2 + e2e[1]**2 + e2e[2]**2)

    def _compute_contour_lenghts(self) -> np.ndarray:
        coordinates = self.get_trajectories_filaments()
        box = self.data_reader.read_box_size()
        box = np.array([box[1, 0] - box[0, 0],
                        box[1, 1] - box[0, 1],
                        box[1, 2] - box[0, 2]])

        filaments = self.get_filaments()
        
        contour_lengths = np.full((len(coordinates), len(filaments[0])), np.nan)

        for t in range(len(coordinates)):
            fil_t = filaments[t]
            for f, fil in enumerate(fil_t):
                fcoords = coordinates[t, fil.items]
                v_segments = geometry.get_minimum_image_vector(fcoords[:-1], fcoords[1:], box)
                d = np.sqrt(np.sum(v_segments**2, 1))
                lc = np.sum(d)
                contour_lengths[t, f] = lc

        return contour_lengths

    def _compute_energies_stretch_and_bend(self) -> np.ndarray:
        coordinates = self.get_trajectories_filaments()
        box = self.data_reader.read_box_size()
        box = np.array([box[1, 0] - box[0, 0],
                        box[1, 1] - box[0, 1],
                        box[1, 2] - box[0, 2]])

        filaments = self.get_filaments()
        filaments_as_tuples = Analyser._convert_nested_filaments_to_tuples(filaments)

        return Analyser._numba_compute_energies_stretch_and_bend(box, coordinates,
                                                                 filaments_as_tuples)

    @staticmethod
    def _convert_nested_filaments_to_tuples(filaments) -> numba.typed.List:
        filaments_as_tuples = numba.typed.List()
        for f_frame in filaments:
            filaments_as_tuples_single_frame = numba.typed.List()
            for f in f_frame:
                filaments_as_tuples_single_frame.append((
                    np.array(f.items).astype('uint32'),
                    np.array(f.motors).astype('uint32')))
            filaments_as_tuples.append(filaments_as_tuples_single_frame)
        return filaments_as_tuples

    @staticmethod
    @numba.njit
    def _numba_compute_energies_stretch_and_bend(
            box, coordinates,
            filaments: numba.typed.List  # List[_FilamentsT]
    ):
        energies = np.zeros((len(coordinates), 2))
        for t in range(len(coordinates)):
            fil_t = filaments[t]
            energies_t = np.zeros((len(fil_t), 2))
            for f, fil in enumerate(fil_t):
                coords_t = coordinates[t]
                fcoords = coords_t[fil[0]]
                v_segments = geometry.get_minimum_image_vector(
                    fcoords[:-1], fcoords[1:], box)
                segment_lengths = np.sqrt(np.sum(v_segments ** 2, 1))

                e_stretch = np.sum((segment_lengths - 1) ** 2)

                cos_theta = ((v_segments[1:] * v_segments[:-1]).sum(1)
                             / segment_lengths[1:] / segment_lengths[:-1])

                e_bend = np.sum(np.arccos(cos_theta) ** 2)

                energies_t[f, 0] = e_stretch
                energies_t[f, 1] = e_bend

            energies[t] = np.sum(energies_t, axis=0)
        return energies

    @staticmethod
    def _keyword_arguments_to_json_string(keyword_arguments: Dict[str, Any]) -> str:
        """
        Note that tuples get hashed. This is to avoid containers with thousands of values
        to become part of the json string, which will be used as key to retrieve
        data from file. Make sure you provide containers with countless items as tuples.
        """
        if not keyword_arguments:
            return ''
        sorted_dict = {}
        for key in sorted(keyword_arguments.keys()):
            value = keyword_arguments[key]
            if isinstance(value, tuple):
                value = 'hashed_tuple_' + str(hash(value))
            sorted_dict[key] = value
        return json.dumps(sorted_dict)

    @staticmethod
    def _check_version(data_set: Dataset):
        if "ACTOMYOSIN_ANALYSER_VERSION" in data_set.attrs:
            if data_set.attrs['ACTOMYOSIN_ANALYSER_VERSION'] != _VERSION:
                msg = "!!!! DataSet '" + data_set.name + "' was created with "
                msg += "actomyosin_analyser version " \
                       + data_set.attrs['ACTOMYOSIN_ANALYSER_VERSION']
                msg += "!\nYour version is " + _VERSION + ".\n"
                msg += "Make sure that the data in here is what you expect it to be."
                warn(msg, RuntimeWarning)
            return
        msg = "!!!! DataSet '" + data_set.name + "' has no version attribute.\n"
        msg += "Make sure that the data in here is what you expect it to be."
        warn(msg, RuntimeWarning)

    @staticmethod
    def _gauss_3D(delta_x: np.ndarray, sigma: np.ndarray) -> np.ndarray:
        return np.exp(-((delta_x/sigma)**2/2).sum(1))

    @staticmethod
    def _get_voxel_mask(bin_indices, grid_range, indices, shape) -> np.ndarray:
        i, j, k = indices
        mask_i = ((np.abs((bin_indices[:, 0]) - i) <= grid_range[0]) |
                  ((-np.abs(bin_indices[:, 0] - i) % shape[0]) <= grid_range[0]))
        mask_j = ((np.abs((bin_indices[:, 1]) - j) <= grid_range[1]) |
                  ((-np.abs(bin_indices[:, 1] - j) % shape[1]) <= grid_range[1]))
        mask_k = ((np.abs((bin_indices[:, 2]) - k) <= grid_range[2]) |
                  ((-np.abs(bin_indices[:, 2] - k) % shape[2]) <= grid_range[2]))
        mask_ijk = (
            mask_i & mask_j & mask_k
        )
        return mask_ijk

    @staticmethod
    def _coordinates_to_bin_indices(coordinates: np.ndarray,
                                    range_x: List[float], width_x: float,
                                    range_y: List[float], width_y: float,
                                    range_z: List[float], width_z: float) -> np.ndarray:
        bin_indices = np.full((len(coordinates), 3), -1, dtype=int)
        for i, (range_i, width) in enumerate(zip([range_x, range_y, range_z],
                                               [width_x, width_y, width_z])):
            mask = (coordinates[:, i] >= range_i[0]) & (coordinates[:, i] <= range_i[1])
            bin_indices[mask, i] = (coordinates[mask, i] - range_i[0]) // width
        return bin_indices

    def __del__(self):
        self.analysis_file.close()

    def _get_filaments_from_analysis_file_or_data_reader(self, save: bool) -> List[List[Filament]]:
        if 'filaments' in self.analysis_file:
            n_frames = len(self.get_time_in_steps())
            return Analyser._load_filaments_from_h5_group(self.analysis_file['filaments'],
                                                          n_frames)
        filaments = self.data_reader.get_filaments_all()
        if save:
            group = self.analysis_file.create_group('filaments')
            Analyser._write_filaments_to_h5_group(group, filaments)
        return filaments

    @staticmethod
    def _load_filaments_from_h5_group(group: h5py.Group, n_frames: int) -> List[List[Filament]]:
        filaments = []
        for f in range(n_frames):
            filaments_f = Analyser._load_filaments_from_h5_group_single_frame(group[str(f)])
            filaments.append(filaments_f)
        return filaments

    @staticmethod
    def _load_filaments_from_h5_group_single_frame(group: h5py.Group) -> List[Filament]:
        items = group['items'][:]
        motors = group['motors'][:]
        filament_tuples = Analyser._parse_items_and_motors_arrays_to_filament_tuples(items, motors)
        filaments = [Filament(list(ftuple[0]), list(ftuple[1])) for ftuple in filament_tuples]
        return filaments

    @staticmethod
    @numba.njit
    def _parse_items_and_motors_arrays_to_filament_tuples(
            items: np.ndarray, motors: np.ndarray
    ) -> _FilamentsT:
        tuples = numba.typed.List()
        assert len(items) == len(motors)
        _invalid = np.iinfo(items.dtype).max
        for i in range(len(items)):
            items_i = items[i]
            items_i = items_i[items_i != _invalid]
            motors_i = motors[i]
            motors_i = motors_i[motors_i != _invalid]
            tuples.append((items_i, motors_i))
        return tuples

    @staticmethod
    def _write_filaments_to_h5_group(group: h5py.Group, filaments: List[List[Filament]]):
        for frame in range(len(filaments)):
            filaments_t = filaments[frame]
            typed_list = numba.typed.List()
            [typed_list.append((np.array(f.items).astype('uint32'),
                                np.array(f.motors).astype('uint32'))) for f in filaments_t]
            group_t = group.create_group(str(frame))
            Analyser._write_filaments_to_h5_group_single_frame(group_t, typed_list)

    @staticmethod
    def _write_filaments_to_h5_group_single_frame(
            group: h5py.Group, filaments: _FilamentsT):
        max_idx, max_items, max_motors = Analyser._get_maximum_items_and_value_for_filaments(filaments)

        items, motors = Analyser._create_filament_item_and_motor_arrays(len(filaments),
                                                                        max_idx,
                                                                        max_items,
                                                                        max_motors)

        Analyser._fill_filament_item_and_motor_arrays(filaments, items, motors)

        group.create_dataset('items', data=items, compression='lzf')
        group.create_dataset('motors', data=motors, compression='lzf')

    @staticmethod
    @numba.njit
    def _fill_filament_item_and_motor_arrays(
            filaments: _FilamentsT,
            items: np.ndarray, motors: np.ndarray):
        for i, (items_i, motors_i) in enumerate(filaments):
            items[i, :len(items_i)] = items_i
            motors[i, :len(motors_i)] = motors_i

    @staticmethod
    @numba.njit
    def _get_maximum_items_and_value_for_filaments(
            filaments: _FilamentsT
    ) -> Tuple[int, int, int]:
        max_items = 0
        max_idx = 0
        max_motors = 0
        for items_i, motors_i in filaments:
            max_idx_f = max(items_i)
            if max_idx_f > max_idx:
                max_idx = max_idx_f
            if len(items_i) > max_items:
                max_items = len(items_i)
            if len(motors_i) > max_motors:
                max_motors = len(motors_i)
        return max_idx, max_items, max_motors

    @staticmethod
    def _create_filament_item_and_motor_arrays(
            n_filaments: int, max_idx: int,
            max_items: int, max_motors:int
    ) -> Tuple[np.ndarray, np.ndarray]:
        dtype = 'uint32'
        _invalid = np.iinfo(dtype).max
        if max_idx > _invalid:
            raise ValueError("can't handle indices larger than "
                             f"{_invalid}, which is the maximum "
                             "for 32 bit unsigned integers")

        items = np.full((n_filaments, max_items), _invalid, dtype=dtype)
        motors = np.full((n_filaments, max_motors), _invalid, dtype=dtype)
        return items, motors




