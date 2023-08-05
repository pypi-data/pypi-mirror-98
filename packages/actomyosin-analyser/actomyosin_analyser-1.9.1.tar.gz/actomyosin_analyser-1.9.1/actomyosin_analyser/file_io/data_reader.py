from abc import ABC, abstractmethod
from typing import Tuple, Dict, List
import numpy as np

from actomyosin_analyser.model.bead import Filament


class DataReader(ABC):
    """
    Template of a data reader class. Any derived class should
    implement the here defined methods.
    This is a place holder to define the interface of a DataReader used
    by the Analyser class. Not all methods have to be overwritten, depending
    on the analyses you perform with the Analyser class.
    """

    @abstractmethod
    def __init__(self, source_file: str):
        ...

    @abstractmethod
    def read_particle_positions(self, minimum_image: bool) -> np.ndarray:
        ...

    @abstractmethod
    def read_time(self) -> np.ndarray:
        ...

    @abstractmethod
    def read_time_as_step_indices(self) -> np.ndarray:
        ...

    @abstractmethod
    def read_box_size(self) -> np.ndarray:
        """
        Read box size in shape (3, 2) where rows are x, y, z,
        columns are lower/upper bound.
        """
        ...

    @abstractmethod
    def read_particle_types(self) -> Tuple[Dict[str, int], np.ndarray]:
        """
        Read particle types as an integer array.
        :return: Dictionary mapping particle type (str) to type as integer.
        :return: Integer array of particle types.
        """
        ...

    @abstractmethod
    def get_filaments_all(self) -> List[List[Filament]]:
        """
        Read filament information for all frames.
        :return: Length of returned list is equal to number of recorded frames.
                 For each frame, each item is a list containing Filament instances.
        """
        ...

    @abstractmethod
    def read_dt(self):
        ...

    @abstractmethod
    def read_parameter(self, *args):
        ...
