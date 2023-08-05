import numpy as np
from typing import List, Dict
from ..model.bead import (Bead, 
                          STATE_FILAMENT_START,
                          STATE_FILAMENT_INTERIOR,
                          STATE_FILAMENT_END)


class BeadStates(object):

    def __init__(self, links_array, filaments_array):
        self.linked_beads = {}
        self.filaments = filaments_array
        self.links = links_array
        
        self.states = self._bead_links_to_states(self.links)
        self._parse_links_to_beads(links_array)

    def get_indices_of_filaments(self) -> Dict[int, List[int]]:
        indices_of_filaments = {}
        for filament in self.filaments[self.filaments[:, 0] != -1]:
            filament_id = filament[0]
            filament_start = filament[1]
            filament_end = filament[2]

            indices = [filament_start]
            current_index = filament_start
            while current_index != filament_end:
                current_index = self.linked_beads[current_index].next
                indices.append(current_index)
            indices_of_filaments[filament_id] = indices
        return indices_of_filaments            

    def _parse_links_to_beads(self, links_array):
        if (links_array.shape[0] % 3 != 0):
            msg = "links_array needs to be multiple of 3 " 
            msg += "(links to previous, next, and cross-linked beads)."            
            raise RuntimeError(msg)
        for i in range(links_array.shape[0] // 3):
            links_i = links_array[i * 3: (i + 1) * 3]            
            if (links_i != -1).any():
                if links_i[0] == links_i[1]:
                    msg = "errors in data: bead " + str(i) \
                          + " has same previous and next neighbour!"
                    raise RuntimeError(msg)
                b = Bead()
                b.previous, b.next, b.cross = links_i                
                self.linked_beads[i] = b

    def _bead_links_to_states(self, links_array):
        if links_array.shape[0] % 3 != 0:
            msg = "links_array' length needs to be multiple of 3 "
            msg += "(links to previous, next beads and across filaments)."
            raise RuntimeError(msg)
        s = np.zeros(links_array.shape[0] // 3)
        for i in range(0, s.shape[0], 1):
            l = links_array[i * 3: (i + 1) * 3]
            if (l == -1).all():
                continue
            if (l[0] != -1) and (l[1] != -1):
                s[i] = STATE_FILAMENT_INTERIOR                
            elif (l[0] != -1) and (l[1] == -1):
                s[i] = STATE_FILAMENT_END
            elif (l[0] == -1) and (l[1] != -1):
                s[i] = STATE_FILAMENT_START
        return s
