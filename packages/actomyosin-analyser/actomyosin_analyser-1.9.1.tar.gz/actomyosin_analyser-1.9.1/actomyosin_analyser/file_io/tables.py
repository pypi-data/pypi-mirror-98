from typing import List
import os
import numpy as np
import pandas as pd

BooleanArray = np.ndarray


def merge_and_save_table(filename: str, table: pd.DataFrame):
    index_cols = list(range(table.index.nlevels))
    if not os.path.exists(filename):
        table.to_csv(filename)
        return
    old_table = pd.read_csv(filename, index_col=index_cols)
    merged_table = _merge_tables(table, old_table)
    merged_table.to_csv(filename)


def _merge_tables(new_table: pd.DataFrame, old_table: pd.DataFrame) -> pd.DataFrame:
    assert (new_table.columns == old_table.columns).all()
    merged_index = _merge_indices(new_table.index, old_table.index)
    df = pd.DataFrame(index=merged_index, columns=new_table.columns)
    df.loc[new_table.index] = new_table
    valid_rows = _get_rows_with_data(old_table)
    diff_index = old_table.index[valid_rows].difference(new_table.index)
    df.loc[diff_index] = old_table.loc[diff_index]
    return df


def _merge_indices(index1, index2) -> pd.Index:
    for name in index1.names:
        assert name in index2.names
        assert index1.get_level_values(name).dtype == index2.get_level_values(name).dtype
    assert len(index1.names) == len(index2.names)
    merged = index1.append(index2.difference(index1))
    return merged


def _get_rows_with_data(table: pd.DataFrame) -> BooleanArray:
    a = np.array(~table.isna())
    return a.sum(axis=1) == table.shape[1]
