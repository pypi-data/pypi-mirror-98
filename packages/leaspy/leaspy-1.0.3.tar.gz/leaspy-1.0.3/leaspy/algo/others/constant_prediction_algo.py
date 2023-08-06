import numpy as np

from leaspy.io.outputs.individual_parameters import IndividualParameters


class ConstantPredictionAlgorithm(): # AbstractAlgo
    """
    Personalization algorithm associated to :class:`~.models.constant_model.ConstantModel`

    It could predict:
        * `last_known`: last non NaN value seen during calibration*§,
        * `last`: last value seen during calibration (even if NaN),
        * `max`: maximum (=worst) value seen during calibration*§,
        * `mean`: average of values seen during calibration§.

    | \\* <!> depending on features, the `last_known` / `max` value may correspond to different visits.
    | § <!> for a given feature, value will be NaN if and only if all values for this feature were NaN.
    """

    _prediction_types = {'last', 'last_known', 'max', 'mean'}

    def __init__(self, settings):
        """
        ConstantPredictionAlgorithm is the algorithm that outputs a constant prediction
        """
        self.name = 'constant_prediction'
        assert settings.name == self.name
        self.features = None
        if settings.parameters['prediction_type'] not in self._prediction_types:
            raise ValueError(f'The `prediction_type` of the constant prediction should be {self._prediction_types}')
        self.prediction_type = settings.parameters['prediction_type']

    def run(self, model, dataset):
        """
        Main method, refer to abstract definition in :meth:`~.algo.personalize.abstract_personalize_algo.AbstractPersonalizeAlgo.run`.

        TODO fix proper inheritance

        Parameters
        ----------
        model : :class:`~.models.constant_model.ConstantModel`
            A subclass object of leaspy `ConstantModel`.
        dataset : :class:`.Dataset`
            Dataset object build with leaspy class objects Data, algo & model

        Returns
        -------
        individual_parameters : :class:`.IndividualParameters`
            Contains individual parameters.
        noise_std: float
            TODO: always 0 for now
        """
        # TODO? we could fit the model before, only to recover model features, and then check at personalize that is the same (as in others personalize algos...)
        self.features = dataset.headers
        model.features = dataset.headers

        ip = IndividualParameters()
        for it in range(dataset.n_individuals):
            idx = dataset.indices[it]
            times = dataset.get_times_patient(it)
            values = dataset.get_values_patient(it).numpy()
            ind_ip = self._get_individual_last_values(times, values)

            ip.add_individual_parameters(str(idx), ind_ip)

        return ip, 0 # TODO? evaluate rmse?

    def _get_individual_last_values(self, times, values):
        """
        Parameters
        ----------
        times : :class:`numpy.ndarray` [float]
            shape (n_visits,)

        values : :class:`numpy.ndarray` [float]
            shape (n_visits, n_features)

        Returns
        -------
        dict[ft_name: str, constant_value_to_be_padded]
        """

        # Return the maximum value
        if self.prediction_type == 'max':
            fts_values = np.nanmax(values, axis=0)

        # Return the mean value
        elif self.prediction_type == 'mean':
            fts_values = np.nanmean(values, axis=0)

        # Return the last or last-known
        else:

            # sort by more recent visits first (= patient is older)
            sorted_indices = sorted(range(len(times)), key=times.__getitem__, reverse=True)

            # Sometimes, last value can be a NaN. If this behavior is intended, then return it anyway
            if self.prediction_type == 'last':
                fts_values = values[sorted_indices[0]]

            else: # == 'last_known'

                values_sorted_desc = values[sorted_indices]

                # get first index of values being non nan, with visits ordered by more recent
                last_non_nan_ix_per_ft = (~np.isnan(values_sorted_desc)).argmax(axis=0)
                # 1 feature value will be nan iff feature was nan at all visits
                fts_values = values_sorted_desc[last_non_nan_ix_per_ft, range(values.shape[1])]

        # return a dict with parameters names being features names
        return dict(zip(self.features, fts_values))


    def set_output_manager(self, settings):
        """
        Not implemented.
        """
        return
