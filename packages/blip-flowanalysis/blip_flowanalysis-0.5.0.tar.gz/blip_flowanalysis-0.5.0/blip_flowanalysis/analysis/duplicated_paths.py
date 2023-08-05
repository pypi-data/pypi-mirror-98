"""Check if bot flow contains duplicated paths.

This is done by class `DuplicatedPaths`.
Class `Sample` make this analysis on a specific pair of states.

Duplicated paths are undesirable on bot flow.
They can make bot maintenance more difficult due to code replication in
different places.
This analyser intends to find if exists duplicated paths and where they are.

A path init on a root state as first level.
Loops are avoided on analysis because states are not considered on a
level if is already on any previous level.
"""
__author__ = 'Gabriel Salgado'
__version__ = '0.2.0'

import typing as tp
import itertools as it
import bisect as bs

from blip_flowanalysis.abstract import Analyser
from blip_flowanalysis.core import Flow
from .comparator.interface_comparator import IComparator
from .comparator.conditions_comparator import ConditionsComparator
from .comparator.actions_comparator import ActionsComparator
from .comparator.outputs_comparator import OutputsComparator
from .comparator.states_comparator import StatesComparator

State = tp.Dict[str, tp.Any]
States = tp.List[State]
Level = tp.List[State]
Path = tp.List[Level]
Context = tp.Tuple[State, State]
MapStates = tp.Dict[str, State]


class Sample(object):
    """Represents a sample for states pairs.
    
    This is a business layer that contains context information (including two
    states) and results (two paths which states are equivalent).
    
    :param comparator: Comparator instance that compares two states.
    :type comparator: `blip_flowanalysis.analysis.comparator.interface_comparator.IComparator`
    :param context: Context input. Includes two initial states to compare.
    :type context: (`dict`, `dict`)
    :param map_states: Mapping state id to state.
    :type map_states: `dict` from `str` to `dict`
    :param min_levels: Minimum levels to detect as duplicated paths.
    :type min_levels: `int`
    """
    
    default_excluded_states = [
        'onboarding',
        'fallback',
    ]
    
    def __init__(
            self,
            comparator: IComparator,
            context: Context,
            map_states: MapStates,
            min_levels: int = 2,
            excluded_states: tp.Optional[tp.List[str]] = None) -> None:
        super().__init__()
        self.comparator = comparator
        self.context = context
        self.map_states = map_states
        self.min_levels = min_levels
        self.excluded_states = excluded_states or self.default_excluded_states
        self.equivalent_paths = self._get_equivalent_paths()
    
    @property
    def state_0(self) -> State:
        return self.context[0]
    
    @property
    def state_id_0(self) -> str:
        return self.state_0['id']
    
    @property
    def state_name_0(self) -> str:
        return self.state_0['name']
    
    @property
    def state_1(self) -> State:
        return self.context[1]
    
    @property
    def state_id_1(self) -> str:
        return self.state_1['id']
    
    @property
    def state_name_1(self) -> str:
        return self.state_1['name']
    
    @property
    def path_0(self) -> Path:
        return self.equivalent_paths[0]
    
    @property
    def path_1(self) -> Path:
        return self.equivalent_paths[1]
    
    @property
    def n_levels(self) -> int:
        return len(self.path_0)
    
    @property
    def n_states(self) -> int:
        return sum(map(len, self.path_0))
    
    @property
    def duplicated_states_0(self) -> States:
        return list(it.chain.from_iterable(self.path_0))

    @property
    def duplicated_states_ids_0(self) -> tp.List[str]:
        return [state['id'] for state in self.duplicated_states_0]
    
    @property
    def duplicated_states_names_0(self) -> tp.List[str]:
        return [state['name'] for state in self.duplicated_states_0]
    
    @property
    def duplicated_states_1(self) -> States:
        return list(it.chain.from_iterable(self.path_1))
    
    @property
    def duplicated_states_ids_1(self) -> tp.List[str]:
        return [state['id'] for state in self.duplicated_states_1]
    
    @property
    def duplicated_states_names_1(self) -> tp.List[str]:
        return [state['name'] for state in self.duplicated_states_1]
    
    def _iterate_state_paths(self, root: State) -> tp.Iterator[States]:
        iterated = list()
        level = [root]
        while level:
            yield level
            for state in level:
                bs.insort(iterated, state['id'])
            current_level = level
            level = list()
            for state in current_level:
                for output in state['outputs']:
                    id_ = output['stateId']
                    index = bs.bisect_left(iterated, id_)
                    if iterated[min(len(iterated) - 1, index)] != id_:
                        level.append(self.map_states[id_])
    
    def _get_equivalent_paths(self) -> tp.Tuple[Path, Path]:
        root_0, root_1 = self.context
        if root_0 in self.excluded_states or root_1 in self.excluded_states:
            return list(), list()
        
        path_0 = self._iterate_state_paths(root_0)
        path_1 = self._iterate_state_paths(root_1)
        equivalent_path_0 = list()
        equivalent_path_1 = list()
        for level_0, level_1 in zip(path_0, path_1):
            equivalent_level_0 = list()
            equivalent_level_1 = list()
            for state_0, state_1 in zip(level_0, level_1):
                if state_0['id'] == state_1['id']:
                    continue
                if state_0['id'] in self.excluded_states:
                    continue
                if state_1['id'] in self.excluded_states:
                    continue
                if self.comparator.compare(state_0, state_1):
                    equivalent_level_0.append(state_0)
                    equivalent_level_1.append(state_1)
            if not equivalent_level_0:
                break
            equivalent_path_0.append(equivalent_level_0)
            equivalent_path_1.append(equivalent_level_1)
        return equivalent_path_0, equivalent_path_1
    
    def is_duplicated(self) -> bool:
        """Evaluate if is duplicated paths case.
        
        :return: `True` if is duplicated paths otherwise `False`.
        :rtype: `bool`
        """
        return len(self.equivalent_paths[0]) >= self.min_levels


Samples = tp.List[Sample]
Results = tp.Tuple[
    States,
    Samples
]

ReportSummary = tp.Dict[str, tp.Any]
ReportDetails = tp.List[tp.Dict[str, tp.Any]]
Report = tp.Dict[str, tp.Any]


class DuplicatedPaths(Analyser):
    """Check if bot flow contains duplicated paths.
    
    Duplicated paths are undesirable on bot flow.
    They can make bot maintenance more difficult due to code replication in
    different places.
    This analyser intends to find if exists duplicated paths and where they
    are.
    
    A path init on a root state as first level.
    Loops are avoided on analysis because states are not considered on a
    level if is already on any previous level.
    
    :param min_levels: Minimum levels to detect as duplicated paths.
    :type min_levels: `int`
    
    :cvar conditions_comparator: Comparator for conditions.
    :type conditions_comparator: `blip_flowanalysis.analysis.comparator.conditions_comparator.ConditionsComparator`
    :cvar actions_comparator: Comparator for actions.
    :type actions_comparator: `blip_flowanalysis.analysis.comparator.actions_comparator.ActionsComparator`
    :cvar outputs_comparator: Comparator for outputs.
    :type outputs_comparator: `blip_flowanalysis.analysis.comparator.outputs_comparator.OutputsComparator`
    :cvar states_comparator: Comparator for states.
    :type states_comparator: `blip_flowanalysis.analysis.comparator.states_comparator.StatesComparator`
    """
    
    conditions_comparator = ConditionsComparator(
        keys=[
            'source',
            'comparison',
            'values',
        ],
    )
    actions_comparator = ActionsComparator(
        conditions_comparator=conditions_comparator,
        map_keys={
            'SendRawMessage': [
                'type',
                'rawContent',
            ],
            'ProcessHttp': [
                'method',
                'headers',
                'uri',
                'body',
            ],
            'TrackEvent': [
                'category',
                'action',
            ],
            'MergeContact': [
                'city',
                'email',
                'expiration',
                'extras',
                'gender',
                'name',
                'phoneNumber',
                'value',
                'variable',
            ],
            'ManageList': [
                'listName',
                'action',
            ],
            'ExecuteScript': [
                'function',
                'source',
            ],
            'SetVariable': [
                'variable',
                'value',
            ],
            'ProcessCommand': [
                'to',
                'method',
                'uri',
            ],
        },
    )
    outputs_comparator = OutputsComparator(
        conditions_comparator=conditions_comparator,
    )
    states_comparator = StatesComparator(
        outputs_comparator=outputs_comparator,
        actions_comparator=actions_comparator,
    )
    default_excluded_states = Sample.default_excluded_states
    
    def __init__(
            self,
            min_levels: int = 2,
            excluded_states: tp.Optional[tp.List[str]] = None) -> None:
        super().__init__()
        self.min_levels = min_levels
        self.excluded_states = excluded_states or self.default_excluded_states
    
    def _sample(self, context: Context, map_states: MapStates) -> Sample:
        return Sample(
            self.states_comparator,
            context,
            map_states,
            self.min_levels,
            self.excluded_states,
        )
    
    def _report_summary(self, results: Results) -> ReportSummary:
        states, samples = results
        n_duplicated_paths = sum(s.is_duplicated() for s in samples)
        n_states = len(states)
        n_irregular_states = len({
            id_
            for s in samples
            if s.is_duplicated()
            for id_ in s.duplicated_states_ids_0 + s.duplicated_states_ids_1
        })
        return {
            'pairs of duplicated paths': n_duplicated_paths,
            'states count': n_states,
            'states on duplicated paths': n_irregular_states,
        }
    
    def _report_details(self, results: Results) -> ReportDetails:
        _, samples = results
        details = list()
        for sample in samples:
            if sample.is_duplicated():
                details.append({
                    'levels quantity': sample.n_levels,
                    'states quantity': sample.n_states,
                    'root 0': {'id': sample.state_id_0, 'name': sample.state_name_0},
                    'root 1': {'id': sample.state_id_1, 'name': sample.state_name_1},
                    'path 0': {
                        f'level {k}': [
                            {'id': state['id'], 'name': state['name']}
                            for state in level
                        ]
                        for k, level in enumerate(sample.path_0)
                    },
                    'path 1': {
                        f'level {k}': [
                            {'id': state['id'], 'name': state['name']}
                            for state in level
                        ]
                        for k, level in enumerate(sample.path_1)
                    },
                })
        return details
    
    def _report(self, results: Results) -> Report:
        summary = self._report_summary(results)
        details = self._report_details(results)
        return {
            'summary': summary,
            'details': details
        }
    
    def analyse(self, flow: Flow) -> Report:
        """Detects duplicated paths on bot flow.
        
        Returns a report with summary and details.
        
        Summary includes:
            * Number of duplicated paths pairs;
            * Number of states;
            * Number of states in some duplicated paths.
        
        For each duplicated paths detection, details includes:
            * Root state id and name of each duplicated path;
            * Levels quantity,
            where a level is outputs of states of previous level;
            * States quantity on each duplicated path;
            * States ids and names of each duplicated path.
        
        :param flow: Bot flow structure.
        :type flow: `blip_flowanalysis.core.Flow`
        :return: Report with analysis of duplicated paths on bot flow.
        :rtype: `dict` from `str` to `any`
        """
        states = flow.get_states_list()
        samples = self.measure(states)
        
        results = states, samples
        return self._report(results)
    
    def measure(self, states: States) -> Samples:
        """Measure all states pairs on bot flow.
        
        Returns a list of samples.
        Each sample is related to a pair of states and gives a result
        including equivalent paths.
        
        See also: `blip_flowanalysis.analysis.duplicated_paths.Sample`.
        
        :param states: List of states on bot flow.
        :type states: `list` of `dict`
        :return: Samples for each states pair.
        :rtype: `list` of `blip_flowanalysis.analysis.duplicated_paths.Sample`
        """
        map_states = {
            state['id']: state
            for state in states
        }
        samples = list()
        
        for root_0, root_1 in it.combinations(states, 2):
            context = root_0, root_1
            sample = self._sample(context, map_states)
            samples.append(sample)
        
        return samples
