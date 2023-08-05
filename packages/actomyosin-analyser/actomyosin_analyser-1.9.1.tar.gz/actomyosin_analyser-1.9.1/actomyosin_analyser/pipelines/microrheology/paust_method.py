from typing import List, Tuple
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from ._g_pipeline import _GPipeline
from .bead_msd import BeadMSD, EnsembleMSDData
from ...tools.experiment_configuration import ExperimentConfiguration
from ...tools.experiment_iterator import GroupIterator
from ...analysis.microrheology.paust_method import (fit_msd,
                                                    paust_model,
                                                    compute_G_via_fit_parameters)
from ...file_io.tables import merge_and_save_table


class PaustMethod(_GPipeline):

    def __init__(self, experiment_configuration: ExperimentConfiguration,
                 skip: int,
                 overwrite: bool=False):
        super().__init__(experiment_configuration, skip)
        self.plot_files.update({
            'PaustFit': os.path.join(experiment_configuration['G'], 'paust_fit_{label}.svg'),
            'G': os.path.join(experiment_configuration['G'], 'G.svg'),
            'G0': os.path.join(experiment_configuration['G0'], 'G_with_G0.svg')
        })
        self.output_files.update({
            'PaustFit': os.path.join(experiment_configuration['G'], 'paust_fit.csv'),
            'G0': os.path.join(experiment_configuration['G0'], 'G0.csv')
        })
        self._bead_msd = BeadMSD(experiment_configuration, skip, overwrite)
        self.skip = skip
        if overwrite:
            self._remove_output_files()

    def run_analysis(self):
        msd_data = self._bead_msd.get_ensemble_msds()
        self._run_paust_analysis(msd_data)

    def _validate_configuration(self):
        assert "G" in self.experiment_configuration
        assert "G0" in self.experiment_configuration

    def _run_paust_analysis(self, msd_data: 'EnsembleMSDData'):
        fit_results = self._fit_paust_model_to_msds(msd_data)
        self._plot_paust_fits(msd_data, fit_results)
        omegas, Gs = PaustMethod._get_omegas_and_Gs_from_fit_parameters(fit_results,
                                                                        msd_data.lag_times,
                                                                        msd_data.bead_radii)
        self._plot_Gs(omegas, Gs, save_file_name=self.plot_files['G'])
        G0s = self._find_G0_via_saddle_point_method(omegas, Gs, self.output_files["G0"])
        self._plot_Gs_with_G0s(omegas, Gs, G0s, self.plot_files['G0'])

    def get_omegas_and_Gs(self) -> Tuple[List[np.ndarray], List[np.ndarray]]:
        msd_data = self._bead_msd.get_ensemble_msds()
        fit_results = self._fit_paust_model_to_msds(msd_data)
        omegas, Gs = PaustMethod._get_omegas_and_Gs_from_fit_parameters(fit_results,
                                                                        msd_data.lag_times,
                                                                        msd_data.bead_radii)
        return omegas, Gs

    def _fit_paust_model_to_msds(self, msd_data: 'EnsembleMSDData') -> pd.DataFrame:
        fit_results = self._create_fit_results_table()

        for i, group in enumerate(self.experiment_configuration.experiment_iterator):
            row = fit_results.iloc[i]
            if row.name[:-1] != tuple(group.values.values()):
                raise RuntimeError("Order of fit results table does not match order"
                                   " of groups.")
            lag_time, msd = msd_data.get_lag_time_and_msd(i)
            parameters, covariance_errors = fit_msd(lag_time, msd)
            fit_results.iloc[i] = parameters
        merge_and_save_table(self.output_files['PaustFit'], fit_results)
        return fit_results.xs(self.skip, level='frames skipped')

    def _create_fit_results_table(self) -> pd.DataFrame:
        index = self._create_group_index_with_skip_index()
        table = pd.DataFrame(index=index, columns=['A', 'B', 'C', 'D'])
        return table

    def _plot_paust_fits(self, msd_data: 'EnsembleMSDData', fit_results: pd.DataFrame):
        groups = self.experiment_configuration.experiment_iterator.groups
        for i in range(msd_data.length):
            lag_time, msd = msd_data.get_lag_time_and_msd(i)
            fit_params = np.array(fit_results.iloc[i])
            self._plot_single_paust_fit(lag_time, msd, fit_params, groups[i])

    def _plot_single_paust_fit(self, lag_time: np.ndarray,
                               msd: np.ndarray,
                               fit_params,
                               group: GroupIterator):
        label = group.label
        file_label = group.get_label_from_values()
        fig, ax = plt.subplots(1, 1)
        filename = self.plot_files['PaustFit'].format(label=file_label)

        ax.plot(lag_time, msd, 'o')
        ax.plot(lag_time, paust_model(lag_time, *fit_params), label='Paust fit')
        ax.legend()
        ax.set(
            title=label,
            xlabel='$\\Delta t / t_0$',
            ylabel='MSD $\\langle \\Delta r^2 \\rangle / x_0^2$',
        )

        fig.savefig(filename)

    @staticmethod
    def _get_omegas_and_Gs_from_fit_parameters(
            fit_results: pd.DataFrame,
            lag_times: List[np.ndarray],
            bead_radii: List[float]
    ) -> Tuple[List[np.ndarray], List[np.ndarray]]:
        omegas, Gs = [], []
        for i in range(len(bead_radii)):
            kT = 1
            bead_radius = bead_radii[i]
            omega = 1/lag_times[i]
            G = compute_G_via_fit_parameters(omega, bead_radius, kT, *np.array(fit_results.iloc[i]))
            omegas.append(omega)
            Gs.append(G)
        return omegas, Gs

