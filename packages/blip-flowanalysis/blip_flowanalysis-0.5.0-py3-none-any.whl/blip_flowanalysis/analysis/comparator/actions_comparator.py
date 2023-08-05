__author__ = 'Gabriel Salgado'
__version__ = '0.1.0'
import typing as tp
import collections as cl

from .interface_comparator import IComparator
from ._specific_comparators import (
    _DictComparator,
    _ElementWithConditionsComparator,
)

Dict = tp.Dict[str, tp.Any]
Action = tp.Dict[str, tp.Any]
Keys = tp.List[str]
MapKeys = tp.Dict[str, Keys]


class ActionsComparator(
        _DictComparator,
        _ElementWithConditionsComparator):
    """Actions comparator.
    
    Compare two actions.
    Equivalency are checked based on keys to compare.
    These keys are mapped according to action type.
    Conditions are also compared.
    """
    
    def __init__(
            self,
            conditions_comparator: IComparator,
            map_keys: MapKeys) -> None:
        super().__init__(conditions_comparator=conditions_comparator)
        self.map_keys = cl.defaultdict(list, map_keys)
    
    def compare(self, left: Action, right: Action) -> bool:
        """Check if two actions are equivalent.
        
        :param left: Action.
        :type left: `dict`
        :param right: Other action.
        :type right: `dict`
        :return: Indication if actions are equivalent.
        :rtype: `bool`
        """
        type = left['type']
        if right['type'] != type:
            return False
        
        keys = self.map_keys[type]
        left_settings = left['settings']
        right_settings = right['settings']
        if not self._compare_dicts(left_settings, right_settings, keys):
            return False
        
        return self._compare_conditions(left, right)
