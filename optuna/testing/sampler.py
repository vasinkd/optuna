import optuna
from optuna import distributions

if optuna.types.TYPE_CHECKING:
    from typing import Dict  # NOQA
    from typing import Union  # NOQA

    from optuna.distributions import BaseDistribution  # NOQA
    from optuna.structs import FrozenTrial  # NOQA
    from optuna.study import InTrialStudy  # NOQA


class DeterministicRelativeSampler(optuna.samplers.BaseSampler):
    def __init__(self, relative_search_space, relative_params):
        # type: (Dict[str, BaseDistribution], Dict[str, float]) -> None

        self.relative_search_space = relative_search_space
        self.relative_params = relative_params

    def infer_relative_search_space(self, study, trial):
        # type: (InTrialStudy, FrozenTrial) -> Dict[str, BaseDistribution]

        return self.relative_search_space

    def sample_relative(self, study, trial, search_space):
        # type: (InTrialStudy, FrozenTrial, Dict[str, BaseDistribution]) -> Dict[str, float]

        return self.relative_params

    def sample_independent(self, study, trial, param_name, param_distribution):
        # type: (InTrialStudy, FrozenTrial, str, BaseDistribution) -> float

        if isinstance(param_distribution, distributions.UniformDistribution):
            param_value = param_distribution.low  # type: Union[float, str]
        elif isinstance(param_distribution, distributions.LogUniformDistribution):
            param_value = param_distribution.low
        elif isinstance(param_distribution, distributions.DiscreteUniformDistribution):
            param_value = param_distribution.low
        elif isinstance(param_distribution, distributions.IntUniformDistribution):
            param_value = param_distribution.low
        elif isinstance(param_distribution, distributions.CategoricalDistribution):
            param_value = param_distribution.choices[0]
        else:
            raise NotImplementedError

        return param_distribution.to_internal_repr(param_value)
