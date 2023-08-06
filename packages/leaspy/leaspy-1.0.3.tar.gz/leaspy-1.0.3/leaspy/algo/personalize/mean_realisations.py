import torch

from .abstract_personalize_algo import AbstractPersonalizeAlgo
from ..samplers.gibbs_sampler import GibbsSampler
from ..samplers.hmc_sampler import HMCSampler
from ...io.outputs.individual_parameters import IndividualParameters


class MeanReal(AbstractPersonalizeAlgo):
    """
    Sampler based algorithm, individual parameters are derivated as the mean realization for `n_samples` samplings.
    """

    def __init__(self, settings):

        # Algorithm parameters
        super().__init__(settings)

    def _initialize_annealing(self):
        if self.algo_parameters['annealing']['do_annealing']:
            if self.algo_parameters['annealing']['n_iter'] is None:
                self.algo_parameters['annealing']['n_iter'] = int(self.algo_parameters['n_iter'] / 2)

        self.temperature = self.algo_parameters['annealing']['initial_temperature']
        self.temperature_inv = 1 / self.temperature

    # TODO cloned --> factorize in a utils ???
    def _initialize_samplers(self, model, data):
        infos_variables = model.random_variable_informations()
        self.samplers = dict.fromkeys(infos_variables.keys())
        for variable, info in infos_variables.items():
            if info["type"] == "individual":
                if self.algo_parameters['sampler_ind'] == 'Gibbs':
                    self.samplers[variable] = GibbsSampler(info, data.n_individuals)
                else:
                    self.samplers[variable] = HMCSampler(info, data.n_individuals, self.algo_parameters['eps'])
            else:
                if self.algo_parameters['sampler_pop'] == 'Gibbs':
                    self.samplers[variable] = GibbsSampler(info, data.n_individuals)
                else:
                    self.samplers[variable] = HMCSampler(info, data.n_individuals, self.algo_parameters['eps'])

    def _get_individual_parameters(self, model, data):

        # Initialize realizations storage object
        realizations_history = []

        # Initialize samplers
        self._initialize_samplers(model, data)

        # Initialize Annealing
        self._initialize_annealing()

        # initialize realizations
        realizations = model.get_realization_object(data.n_individuals)
        realizations.initialize_from_values(data.n_individuals, model)

        # Gibbs sample n_iter times
        for i in range(self.algo_parameters['n_iter']):
            for key in realizations.reals_ind_variable_names:
                self.samplers[key].sample(data, model, realizations, self.temperature_inv)

            # Append current realizations if burn in is finished
            if i > self.algo_parameters['n_burn_in_iter']:
                realizations_history.append(realizations.copy())

        # Compute mean of n_iter realizations for each individual variable
        mean_output = dict.fromkeys(model.get_individual_variable_name())
        for name_variable, info_variable in model.random_variable_informations().items():
            if info_variable['type'] == 'individual':
                mean_variable = torch.stack(
                    [realizations[name_variable].tensor_realizations for realizations in realizations_history]).mean(
                    dim=0).clone().detach()
                mean_output[name_variable] = mean_variable

        # Compute the attachment
        realizations = model.get_realization_object(data.n_individuals)
        for key, value in mean_output.items():
            realizations[key].tensor_realizations = value

        # Get individual realizations from realizations object
        param_ind = model.get_param_from_real(realizations)

        ### TODO : The following was adding for the conversion from Results to IndividualParameters. Everything should be changed

        individual_parameters = IndividualParameters()
        p_names = list(param_ind.keys())
        n_sub = len(param_ind[p_names[0]])

        for i in range(n_sub):
            p_dict = {k: param_ind[k][i].numpy() for k in p_names}
            p_dict = {k: v[0] if v.shape[0] == 1 else v.tolist() for k, v in p_dict.items()}
            individual_parameters.add_individual_parameters(str(i), p_dict)

        return individual_parameters
