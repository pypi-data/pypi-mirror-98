import os
import warnings

import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch

from leaspy.io.outputs.individual_parameters import IndividualParameters
# import matplotlib.backends.backend_pdf


# TODO: outdated -
class Plotting:

    def __init__(self, model, output_path='.', palette='tab10', max_colors=10):
        self.model = model

        # ---- Graphical options
        self.color_palette = None
        self.standard_size = (8, 4)
        self.linestyle = {'average_model': '-', 'individual_model': '-', 'individual_data': '-'}
        self.linewidth = {'average_model': 5, 'individual_model': 2, 'individual_data': 2}
        self.alpha = {'average_model': 0.5, 'individual_model': 1, 'individual_data': 1}
        self.output_path = output_path

        self.set_palette(palette, max_colors)

    def update_model(self, model):
        self.model = model

    def set_palette(self, palette, max_colors=None):
        """
        Set palette of plots

        Parameters
        ----------
        palette : str (palette name) or :class:`matplotlib.colors.Colormap` (`ListedColormap` or `LinearSegmentedColormap`)

        max_colors : int > 0, optional (default, corresponding to model nb of features)
            Only used if palette is a string
        """

        if isinstance(palette, mpl.colors.Colormap):
            self.color_palette = palette
        else:
            if max_colors is None:
                assert self.model.dimension is not None, "Initialize model first please"
                max_colors = self.model.dimension
            self.color_palette = cm.get_cmap(palette, max_colors)

    def colors(self, at=None):
        """
        Wrapper over color_palette iterator to get colors

        Parameters
        ----------
        at : any legit color_palette arg (int, float or iterable of any of these) or None (default)
            if None returns all colors of palette upto model dimension

        Returns
        -------
        colors : single color tuple (RGBA) or np.array of RGBA colors (number of colors x 4)
        """
        if at is None:
            at = [i % self.color_palette.N for i in range(self.model.dimension)]

        return self.color_palette(at)

    def _raise_if_model_not_init(self):
        # /!\ Break if model is not initialized
        if not self.model.is_initialized:
            raise ValueError("Please initialize the model before plotting")

    def _handle_kwargs_begin(self, kwargs, all_features_list = None):

        # get features from initialized model if not set
        if all_features_list is None:
            self._raise_if_model_not_init()
            all_features_list = self.model.features

        # ---- Get requested features (may be a subset)
        features = kwargs.get('features', all_features_list)
        features_ix = list(map(all_features_list.index, features))

        # ---- Colors
        colors = kwargs.get('color', self.colors(features_ix))
        assert len(colors) >= len(features)
        # TODO: reindex default colors if subset of features?

        # ---- Labels
        labels = kwargs.get('labels', features)
        assert len(labels) == len(features)

        # ---- Ax
        ax = kwargs.get('ax', None)
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=kwargs.get('figsize', self.standard_size))

        # ---- Handle ylim
        if 'logistic' in self.model.name:
            ax.set_ylim(0, 1)

        return ax, features, features_ix, labels, colors

    def _handle_kwargs_end(self, ax, kwargs, colors, labels):
        # ---- Legend
        dimension = len(labels)
        #if dimension is None:
        #    dimension = self.model.dimension

        custom_lines = [mpl.lines.Line2D([0], [0], color=colors[i], lw=4) for i in range(dimension)]
        ax.legend(custom_lines, labels, title='Features')
        # ax.legend(title='Features')
        ax.set_ylabel('Normalized score')

        # ---- Save
        if 'save_as' in kwargs.keys():
            plt.savefig(os.path.join(self.output_path, kwargs['save_as']))

    def average_trajectory(self, **kwargs):
        """
        Plot the population average trajectories. They are parametrized by the population parameters derivated
        during the calibration.

        Parameters
        ----------
        kwargs
            * alpha: float, default 0.6
                Matplotlib's transparency option. Must be in [0, 1].
            * linestyle: {'-', '--', '-.', ':', '', (offset, on-off-seq), ...}
                Matplotlib's linestyle option.
            * linewidth: float
                Matplotlib's linewidth option.
            * features: list[str]
                Name of features (if set it must be a subset of model features)
                Default: all model features.
            * colors: list[str]
                Contains matplotlib compatible colors.
                At least as many as number of features.
            * labels: list[str]
                Used to rename features in the plot.
                Exactly as many as number of features.
                Default: raw variable name of each feature
            * ax: matplotlib.axes.Axes
                Axes object to modify, instead of creating a new one.
            * figsize: tuple of int
                The figure's size.
            * save_as: str, default None
                Path to save the figure.
            * title: str
            * n_tpts: int
                Nb of timpepoints in plot (default: 100)
            * n_std_left, n_std_right: float (default: 3 and 6 resp.)
                Time window around `tau_mean`, expressed as times of max(`tau_std`, 4)

        Returns
        -------
        ax: matplotlib.axes.Axes
        """
        # ---- Input manager
        plot_kws = self._plot_kwargs('average', kwargs)

        ax, _, features_ix, labels, colors = self._handle_kwargs_begin(kwargs)

        # ---- Get timepoints
        mean_time = self.model.parameters['tau_mean'].item()
        std_time = max(self.model.parameters['tau_std'].item(), 4)
        timepoints = mean_time + std_time * np.linspace(-kwargs.get('n_std_left', 3), kwargs.get('n_std_right', 6), kwargs.get('n_tpts', 100))
        timepoints = torch.tensor([timepoints], dtype=torch.float32)

        # ---- Compute average trajectory
        mean_trajectory = self.model.compute_mean_traj(timepoints).detach().numpy()

        # ---- plot it for each dimension
        for ft_ix, ft_lbl, ft_color in zip(features_ix, labels, colors):
            ax.plot(timepoints[0, :].detach().numpy(),
                    mean_trajectory[0, :, ft_ix],
                    c=ft_color,
                    #label=ft_lbl, # not needed
                    **plot_kws['model'])

        # ---- Title & labels
        ax.set_title('Average trajectories')
        ax.set_xlabel('Age')

        self._handle_kwargs_end(ax, kwargs, colors, labels)

        return ax

    def _plot_kwargs(self, case, kwargs):

        if case == 'average':
            return {'model':
                dict(
                    alpha = kwargs.get('alpha', self.alpha['average_model']),
                    linestyle = kwargs.get('linestyle', self.linestyle['average_model']),
                    linewidth = kwargs.get('linewidth', self.linewidth['average_model'])
                )}
        elif case == 'obs':
            return {'obs':
                dict(
                    alpha = kwargs.get('alpha', self.alpha['individual_data']),
                    linestyle = kwargs.get('linestyle', self.linestyle['individual_data']),
                    linewidth = kwargs.get('linewidth', self.linewidth['individual_data']),
                    marker = kwargs.get('marker', 'o'),
                    markersize = kwargs.get('markersize', '3'),
                )}
        elif case == 'recons':
            # both observations & model will be displayed
            p_obs = dict(
                marker = kwargs.get('marker', 'o'), # None not to display obs
                markersize = kwargs.get('markersize', '3'),
                alpha = kwargs.get('obs_alpha', self.alpha['individual_data']),
                linestyle = kwargs.get('obs_ls', ''),
                linewidth = kwargs.get('obs_lw', self.linewidth['individual_data']),
            )
            p_model = dict(
                alpha = kwargs.get('alpha', self.alpha['individual_model']),
                linestyle = kwargs.get('linestyle', self.linestyle['individual_model']),
                linewidth = kwargs.get('linewidth', self.linewidth['individual_model']),
            )
            return {'obs': p_obs, 'model': p_model}
        else:
            raise NotImplementedError

    @staticmethod
    def _get_ip_df_torch(individual_parameters):
        # convert individual parameters in different cases

        if isinstance(individual_parameters, IndividualParameters):
            ip_df = individual_parameters.to_dataframe()
            ip_torch = individual_parameters.to_pytorch()
        elif isinstance(individual_parameters, pd.DataFrame):
            ip_df = individual_parameters
            ip_torch = IndividualParameters.from_dataframe(individual_parameters).to_pytorch()
        elif isinstance(individual_parameters, tuple):
            ip_df = IndividualParameters.from_pytorch(*individual_parameters).to_dataframe()
            ip_torch = individual_parameters
        else:
            raise ValueError("`individual_parameters` should be an IndividualParameters object, a pandas.DataFrame or a dict.")

        return ip_df, ip_torch

    def _plot_patients_generic(self, case, data, patients_idx='all', individual_parameters=None, reparametrized_ages=False, **kwargs):

        # plot with reparametrized ages
        if individual_parameters is not None:
            self._raise_if_model_not_init()
            ip_df, ip_torch = self._get_ip_df_torch(individual_parameters)

        # ---- Input manager
        plot_kws = self._plot_kwargs(case, kwargs)
        with_model = 'model' in plot_kws # plot reconstruction of model as well
        with_obs = 'obs' in plot_kws and plot_kws['obs'].get('marker') is not None
        assert with_model or with_obs # (or both !)

        # ---- Patients sublist
        if 'patient_IDs' in kwargs.keys():
            warnings.warn("Keyword argument <patient_IDs> is deprecated! "
                          "Use <patients_idx> instead.", DeprecationWarning)
            patients_idx = kwargs.get('patient_IDs')

        if isinstance(patients_idx, str):
            if patients_idx == 'all':
                patients_idx = list(data.iter_to_idx.values())
            else:
                patients_idx = [patients_idx]

        # features check
        if self.model.is_initialized:
            assert data.headers == self.model.features

        ax, features, features_ix, labels, colors = self._handle_kwargs_begin(kwargs, data.headers)

        # Data to dataframe (only selected patients)
        df = data.to_dataframe().reset_index().set_index('ID').loc[patients_idx]

        if reparametrized_ages:
            assert ip_df is not None
            t0 = self.model.parameters['tau_mean'].item()
            df = df.join(ip_df)
            # reparametrized ages
            df['TIME_reparam'] = np.exp(df['xi']) * (df['TIME'] - df['tau']) + t0

        # ---- Plot

        # plot observations (with reparametrized times or not)
        if with_obs:
            self._plot_observations(ax, df, features, colors, reparametrized_ages, plot_kws['obs'])

        # plot reconstruction as well (model values)
        if with_model:
            assert ip_torch is not None
            self._plot_model_trajectories(ax, df, self.model, ip_torch, features_ix, colors, reparametrized_ages, plot_kws['model'], **kwargs)

        # ---- Title & labels
        if with_obs:
            title = 'Observations'
            if with_model:
                title += ' and individual trajectories'
        else: # only with_model
            title = 'Individual trajectories'
        ax.set_title(title)

        if reparametrized_ages:
            ax.set_xlabel('Reparametrized age')
        else:
            ax.set_xlabel('Age')

        self._handle_kwargs_end(ax, kwargs, colors, labels)

        return ax

    @staticmethod
    def _plot_observations(ax, df, features, colors, reparametrized_ages, plot_kws):
        """
        Internal routine: plot individual observations

        Parameters
        ----------
        ax: matplotlib ax
        df : :class:`pandas.DataFrame`
            Data to plot
        features: list[str]
            Which features to plot (subset of model features / data features)
        colors: list
            List of colors (associated to features selected), in order
        reparametrized_ages: bool
            Should we plot trajectories in reparam age or not?
        plot_kws: dict
            Plot kwargs
        """

        if reparametrized_ages:
            time_col = 'TIME_reparam'
        else:
            time_col = 'TIME'

        for ind_id, ind_df in df.groupby('ID'):

            timepoints = ind_df[time_col] # reparametrized before if needed
            observations = ind_df[features] # selected features only

            for (ft_name, s_ind_ft), ft_color in zip(observations.items(), colors):

                ft_not_nans = s_ind_ft.notnull()

                ax.plot(timepoints[ft_not_nans],
                        s_ind_ft[ft_not_nans],
                        c=ft_color,
                        #label=ft_lbl, # legend is done afterwards
                        **plot_kws)

    @staticmethod
    def _plot_model_trajectories(ax, df, model, individual_parameters, features_ix, colors, reparametrized_ages, plot_kws, **kwargs):
        """
        Internal routine: plot individual trajectories estimated by model

        Parameters
        ----------
        ax: matplotlib ax
        df : :class:`pandas.DataFrame`
            Data (TODO: could be the MultiIndex [ID,TIME] instead...)
        individual_parameters: tuple[list, dict]
            <!> in pytorch dict format: tuple(indices:list, dict{ip_name: vals})
        features_ix: list[int]
            Which features to plot (order of features from model)
        colors: list
            List of colors (associated to features selected), in order
        reparametrized_ages: bool
            Should we plot trajectories in reparam age or not?
        plot_kws: dict
            Plot kwargs
        kwargs:
            * "factor_past", "factor_future": float (default 0.5)
                past/future padding to plot (as fraction of total follow-up duration of subjects)
            * "n_tpts": int (default 100)
                nb of tpts in trajectory
        """

        ip_indices, ip_torch = individual_parameters

        for ind_id, ind_df in df.groupby('ID'):

            ind_ix = ip_indices.index(ind_id)
            ind_ip = {pn: pv[ind_ix] for pn, pv in ip_torch.items()} # torch compatible

            timepoints = ind_df['TIME'] # <!> always real patient ages here (to compute)
            min_t, max_t = min(timepoints), max(timepoints)
            total_t = max_t - min_t

            timepoints = np.linspace(min_t - kwargs.get('factor_past', .5) * total_t, max_t + kwargs.get('factor_future', .5) * total_t, kwargs.get('n_tpts', 100))
            t = torch.tensor(timepoints, dtype=torch.float32).unsqueeze(0)

            trajectory = model.compute_individual_tensorized(t, ind_ip).squeeze(0)

            # times to plot if reparametrized ages are wanted
            if reparametrized_ages:
                timepoints = (model.time_reparametrization(t, ind_ip['xi'], ind_ip['tau']) + model.parameters['tau_mean'].item()).squeeze(0).numpy()

            for ft_ix, ft_color in zip(features_ix, colors):
                ax.plot(timepoints,
                        trajectory[:, ft_ix],
                        c=ft_color,
                        #label=ft_lbl,
                        **plot_kws
                        )

    def patient_observations(self, data, patients_idx = 'all', individual_parameters = None, **kwargs):
        """
        Plot patient observations

        Parameters
        ----------
        data : :class:`.Data`
        patients_idx: 'all' (default), str or list[str]
            Patients to display (by their ID).
        individual_parameters : :class:`.IndividualParameters` or :class:`pandas.DataFrame` (as may be outputed by ip.to_dataframe()) or dict (Pytorch ip format) or None (default)
            If not None, observations are plotted with respect to reparametrized ages.
        """

        return self._plot_patients_generic('obs', data, patients_idx = patients_idx, individual_parameters = individual_parameters, reparametrized_ages = individual_parameters is not None, **kwargs)

    def patient_observations_reparametrized(self, data, individual_parameters, patients_idx = 'all', **kwargs):
        """
        Plot patient observations (reparametrized ages)

        cf. `patient_observations`, uniquely a reordering of arguments (and mandatory `individual_parameters`) for ease of use...
        """

        return self._plot_patients_generic('obs', data, patients_idx = patients_idx, individual_parameters = individual_parameters, reparametrized_ages = True, **kwargs)


    def patient_trajectories(self, data, individual_parameters, patients_idx, reparametrized_ages = False, **kwargs):
        """
        Plot patient observations together with model individual reconstruction

        Parameters
        ----------
        data : :class:`.Data`
        individual_parameters : :class:`.IndividualParameters` or :class:`pandas.DataFrame` (as may be outputed by ip.to_dataframe()) or dict (Pytorch ip format)
        patients_idx: 'all' (default), str or list[str]
            Patients to display (by their ID).
        reparametrized_ages: bool (default False)
            Should we plot trajectories in reparam age or not? to study source impact essentially
        kwargs:
            cf. `_plot_model_trajectories`
            In particular, pass marker=None if you don't want observations besides model
        """

        return self._plot_patients_generic('recons', data, patients_idx = patients_idx, individual_parameters = individual_parameters, reparametrized_ages = reparametrized_ages, **kwargs)


