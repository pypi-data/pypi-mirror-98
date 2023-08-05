import numpy as np
from math import isclose
from typing import List


def split_filament_coords_at_borders(ordered_bead_coords: np.ndarray, box) -> List[np.ndarray]:
    """
    @param ordered_bead_coords Coordinates of beads, have to be corrected via minimum image!
    """
    coordinate_sets = []
    diff = ordered_bead_coords[1:] - ordered_bead_coords[:-1]
    shifts = _compute_shifts_array(diff, box)
    shifts_at = np.where(shifts != 0)
    if len(shifts_at[0]) == 0:
        return [ordered_bead_coords]
    shifts_at_n, shifts_at_i, r_cuts = _sort_conflicting_shifts(shifts_at[0], shifts_at[1],
                                                                ordered_bead_coords, diff,
                                                                shifts, box)
    shifted_diffs = diff + shifts
    n_prev = shifts_at_n[0]
    prev_virtual_bead = None

    coord_set, prev_virtual_bead = _generate_coord_set_before_first_split(
        ordered_bead_coords[:shifts_at_n[0] + 1], n_prev, r_cuts[0], shifted_diffs)
    coordinate_sets.append(coord_set)
    for j, n in enumerate(shifts_at_n[1:]):
        j = j+1
        set_shape = list(ordered_bead_coords.shape)
        if n == n_prev:
            num_points = 2
        else:
            num_points = n - n_prev + 2
        set_shape[0] = num_points
        coord_set = np.empty(tuple(set_shape))
        if prev_virtual_bead is not None:
            prev_i = shifts_at_i[j-1]
            if isclose(prev_virtual_bead[prev_i], box[prev_i], abs_tol=box[prev_i] * 0.01):
                prev_virtual_bead[prev_i] -= box[prev_i]
            else:
                prev_virtual_bead[prev_i] += box[prev_i]
            coord_set[0] = prev_virtual_bead
        if n == n_prev:
            virtual_bead = coord_set[0] + (r_cuts[j] - r_cuts[j-1]) * shifted_diffs[n]
        else:
            coord_set[1: -1] = ordered_bead_coords[n_prev+1: n+1]
            virtual_bead = ordered_bead_coords[n] + r_cuts[j] * shifted_diffs[n]
        prev_virtual_bead = virtual_bead
        coord_set[-1] = virtual_bead

        coordinate_sets.append(coord_set)
        n_prev = n
        
    coord_set = _generate_coord_set_after_last_split(
        ordered_bead_coords, n_prev, shifts_at_i, prev_virtual_bead, box)
    
    coordinate_sets.append(coord_set)
    
    return coordinate_sets

def _generate_coord_set_before_first_split(bead_coords_before_split, n, r_cut, shifted_diffs):
    coord_set_shape = list(bead_coords_before_split.shape)
    coord_set_shape[0] = coord_set_shape[0] + 1
    coord_set = np.empty(tuple(coord_set_shape))
    coord_set[:-1] = bead_coords_before_split[:]
    virtual_bead = bead_coords_before_split[-1] + r_cut * shifted_diffs[n]
    coord_set[-1] = virtual_bead
    return coord_set, virtual_bead
    

def _generate_coord_set_after_last_split(ordered_bead_coords, n_prev,
                                         shifts_at_i, prev_virtual_bead, box):
    num_points = len(ordered_bead_coords) - n_prev
    set_shape = list(ordered_bead_coords.shape)
    set_shape[0] = num_points
    coord_set = np.empty(tuple(set_shape))
    last_i = shifts_at_i[-1]
    if isclose(prev_virtual_bead[last_i], box[last_i], abs_tol=box[last_i] * 0.01):
        prev_virtual_bead[last_i] -= box[last_i]
    else:
        prev_virtual_bead[last_i] += box[last_i]
    coord_set[0] = prev_virtual_bead
    coord_set[1:] = ordered_bead_coords[n_prev+1:]
    return coord_set

def _compute_shifts_array(diff, box):
    shifts = np.zeros_like(diff)
    for i, b in enumerate(box):
        if b is None:            
            continue
        shifts_i = -b * np.rint(diff[:, i] / b)
        shifts[:, i] = shifts_i
    return shifts
        
def _sort_conflicting_shifts(shifts_at_n, shifts_at_i,
                             ordered_bead_coords, diff, shifts, box):

    r_cuts = np.zeros(shifts_at_n.shape)
    for j in range(len(shifts_at_n)):
        conflicting_indices = []
        nj = shifts_at_n[j]
        k = j + 1
        while k < len(shifts_at_n):
            nk = shifts_at_n[k]
            if nj != nk:
                break
            conflicting_indices.append(k)
            k += 1
        if len(conflicting_indices) == 0:
            ij = shifts_at_i[j]
            dx = diff[nj, ij] + shifts[nj, ij]
            x_nj_ij = ordered_bead_coords[nj, ij]
            if x_nj_ij + dx > box[ij]:
                r_cut = abs((box[ij] - x_nj_ij) / dx)
            else:                
                r_cut = abs(x_nj_ij / dx)
            r_cuts[j] = r_cut
            continue
        conflicting_indices.insert(0, j)
        boundary_cuts = {}
        for l in conflicting_indices:
            nl = shifts_at_n[l]
            il = shifts_at_i[l]
            dx = diff[nl, il] + shifts[nl, il]
            x_nl_il = ordered_bead_coords[nl, il]
            if x_nl_il + dx > box[il]:
                r_cut = abs((box[il] - x_nl_il) / dx)
            else:                
                r_cut = abs(x_nl_il / dx)
            boundary_cuts[l] = r_cut
        sorted_boundary_cut_pairs = sorted(boundary_cuts.items(), key=lambda x: x[1])

        conflicting_shifts_in_correct_order_n = []
        conflicting_shifts_in_correct_order_i = []
        r_cuts_in_correct_order = []
        # a cut pair is a Tuple of the index in the shifts_at array and the r_cut value
        for cut_pair in sorted_boundary_cut_pairs:
            conflicting_shifts_in_correct_order_n.append(shifts_at_n[cut_pair[0]])
            conflicting_shifts_in_correct_order_i.append(shifts_at_i[cut_pair[0]])
            r_cuts_in_correct_order.append(cut_pair[1])
        shifts_at_n[j:j+len(conflicting_indices)] = conflicting_shifts_in_correct_order_n
        shifts_at_i[j:j+len(conflicting_indices)] = conflicting_shifts_in_correct_order_i
        r_cuts[j:j+len(conflicting_indices)] = r_cuts_in_correct_order
    return shifts_at_n, shifts_at_i, r_cuts
