from leaspy.models.lme_model import LMEModel
import numpy as np

from leaspy.algo.abstract_algo import AbstractAlgo
from leaspy.io.outputs.individual_parameters import IndividualParameters
import statsmodels.api as sm


class LMEPersonalizeAlgorithm(AbstractAlgo):
    r"""
    Personalization algorithm associated to :class:`~.models.lme_model.LMEModel`

    Attributes
    ----------
    name : ``'lme_personalize'``

    """

    def __init__(self, settings):
        self.name = 'lme_personalize'
        assert settings.name == self.name

    def run(self, model, dataset):
        """
        Main method, refer to abstract definition in :meth:`~.algo.personalize.abstract_personalize_algo.AbstractPersonalizeAlgo.run`.

        TODO fix proper inheritance

        Parameters
        ----------
        model : :class:`~.models.lme_model.LMEModel`
            A subclass object of leaspy `LMEModel`.
        dataset : :class:`.Dataset`
            Dataset object build with leaspy class objects Data, algo & model

        Returns
        -------
        individual_parameters : :class:`.IndividualParameters`
            Contains individual parameters.
        noise_std: float
            The estimated noise
        """

        if model.features != dataset.headers:
            raise ValueError(
                "LME model was not fitted on the same features than those you want to personalize on. "
                "Model features : {}, data features: {}".format(model.features, dataset.headers))

        ip = IndividualParameters()
        residuals = []
        for it in range(dataset.n_individuals):
            idx = dataset.indices[it]
            times = dataset.get_times_patient(it)
            values = dataset.get_values_patient(it).numpy()

            ind_ip, ind_residuals = self._get_individual_random_effects_and_residuals(model, times, values)

            residuals.append(ind_residuals)

            ip.add_individual_parameters(str(idx), ind_ip)

        # stacked residuals
        rmse = (np.hstack(residuals) ** 2).mean() ** .5

        return ip, rmse

    @staticmethod
    def _remove_nans(values, times):
        values = values.flatten()
        mask = ~np.isnan(values)
        values = values[mask]
        times = times[mask]
        return values, times

    @classmethod
    def _get_individual_random_effects_and_residuals(cls, model: LMEModel, times, values):

        values, times = cls._remove_nans(values, times)

        ages_norm = (times - model.parameters['ages_mean']) / model.parameters['ages_std']

        X = sm.add_constant(ages_norm, prepend=True, has_constant='add')
        residuals = values - X @ model.parameters['fe_params']

        cov_re_unscaled_inv = model.parameters['cov_re_unscaled_inv']

        if not model.with_random_slope_age:
            # only valid with random intercept ("Z"=[1,...,1] and cov_re is a scalar)
            n = len(values) # number of effective observations
            random_intercept = np.sum(residuals) / (n + cov_re_unscaled_inv.item())

            re_d = {'random_intercept': random_intercept}

            residuals = residuals - random_intercept
        else:
            # valid anytime (exog_re = X)
            re = cls._generic_get_random_effects(residuals, X, cov_re_unscaled_inv).squeeze()

            re_d = {'random_intercept': re[0], 'random_slope_age': re[1]}

            residuals = residuals - X @ re

        return re_d, residuals


    @staticmethod
    def _generic_get_random_effects(resid, Z, cov_re_unscaled_inv):
        """
        The conditional means of random effects given the data.
        cf. http://sia.webpopix.org/lme.html#estimation-of-the-random-effects

        Parameters
        ----------
        resid : :class:`numpy.ndarray` (n_i,)
            endog - fixed_effects * exog
        Z : :class:`numpy.ndarray` (n_i, k_re)
            exog_re
        cov_re_unscaled_inv : :class:`numpy.ndarray` (k_re, k_re)
            inverse

        Returns
        -------
        random_effects : :class:`numpy.ndarray` (k_re,)
            For a given individual
        """

        tZZ = np.dot(Z.T, Z)
        G = np.linalg.inv(tZZ + cov_re_unscaled_inv)
        return np.dot(G, np.dot(Z.T, resid)) # less costly to multiply in this order

    def set_output_manager(self, settings):
        """
        Not implemented.
        """
        return
