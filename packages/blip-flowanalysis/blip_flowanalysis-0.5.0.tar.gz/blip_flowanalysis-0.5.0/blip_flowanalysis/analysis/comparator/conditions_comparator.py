__author__ = 'Gabriel Salgado'
__version__ = '0.1.0'
import typing as tp

from ._specific_comparators import _DictComparator

Dict = tp.Dict[str, tp.Any]
Condition = tp.Dict[str, tp.Any]
Keys = tp.List[str]


class ConditionsComparator(_DictComparator):
    """Conditions comparator.
    
    Compare two conditions.
    """
    
    def __init__(self, keys: Keys) -> None:
        super().__init__()
        self.keys = keys
    
    def compare(self, left: Condition, right: Condition) -> bool:
        """Check if two conditions are equivalent.
        
        :param left: Condition.
        :type left: `dict`
        :param right: Other condition.
        :type right: `dict`
        :return: Indication if conditions are equivalent.
        :rtype: `bool`
        """
        return self._compare_dicts(left, right, self.keys)
