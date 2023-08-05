__author__ = 'Gabriel Salgado'
__version__ = '0.1.0'
import abc
import typing as tp
import itertools as it

from .interface_comparator import IComparator

Dict = tp.Dict[str, tp.Any]
Output = tp.Dict[str, tp.Any]
Keys = tp.List[str]
MapKeys = tp.Dict[str, Keys]


class _DictComparator(IComparator, abc.ABC):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
    
    def _compare_dicts(self, left: Dict, right: Dict, keys: Keys) -> bool:
        left = {
            k: left[k]
            for k in keys
            if k in left
        }
        right = {
            k: right[k]
            for k in keys
            if k in right
        }
        return left == right


class _ElementWithConditionsComparator(IComparator, abc.ABC):
    
    def __init__(
            self,
            conditions_comparator: IComparator, **kwargs) -> None:
        super().__init__(**kwargs)
        self.conditions_comparator = conditions_comparator
    
    def _compare_conditions(self, left: Output, right: Output) -> bool:
        left_conditions = left.get('conditions', list())
        right_conditions = right.get('conditions', list())
        if len(left_conditions) != len(right_conditions):
            return False
        
        return all(it.starmap(
            self.conditions_comparator.compare,
            zip(left_conditions, right_conditions)
        ))
