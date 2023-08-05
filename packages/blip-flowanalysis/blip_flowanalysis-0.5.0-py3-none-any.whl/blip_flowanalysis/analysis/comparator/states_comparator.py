__author__ = 'Gabriel Salgado'
__version__ = '0.1.0'
import typing as tp
import itertools as it

from .interface_comparator import IComparator

State = tp.Dict[str, tp.Any]
Output = tp.Dict[str, tp.Any]
Outputs = tp.List[Output]
Action = tp.Dict[str, tp.Any]
Actions = tp.List[Action]


class StatesComparator(IComparator):
    """States comparator.
    
    Compare two states.
    Actions and outputs are compared.
    """
    
    def __init__(
            self,
            outputs_comparator: IComparator,
            actions_comparator: IComparator,
            outputs_key: str = 'outputs',
            actions_io: tuple = ('inputActions', 'outputActions')) -> None:
        super().__init__()
        self.outputs_comparator = outputs_comparator
        self.actions_comparator = actions_comparator
        self.outputs_key = outputs_key
        self.actions_io = actions_io
    
    def _compare_outputs(self, left: Outputs, right: Outputs) -> bool:
        if len(left) != len(right):
            return False
        return all(it.starmap(
            self.outputs_comparator.compare,
            zip(left, right)))
    
    def _compare_actions(self, left: Actions, right: Actions) -> bool:
        if len(left) != len(right):
            return False
        return all(it.starmap(
            self.actions_comparator.compare,
            zip(left, right)))
    
    def compare(self, left: State, right: State) -> bool:
        """Check if two states are equivalent.
        
        :param left: State.
        :type left: `dict`
        :param right: Other state.
        :type right: `dict`
        :return: Indication if states are equivalent.
        :rtype: `bool`
        """
        left_outputs = left[self.outputs_key]
        right_outputs = right[self.outputs_key]
        equal_outputs = self._compare_outputs(left_outputs, right_outputs)
        if not equal_outputs:
            return False
        
        for action_interface in self.actions_io:
            left_actions = left[action_interface]
            right_actions = right[action_interface]
            equal_actions = self._compare_actions(left_actions, right_actions)
            if not equal_actions:
                return False
        return True
