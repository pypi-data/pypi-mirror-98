__author__ = 'Gabriel Salgado'
__version__ = '0.1.0'
import typing as tp

from .interface_comparator import IComparator
from ._specific_comparators import _ElementWithConditionsComparator

Dict = tp.Dict[str, tp.Any]
Output = tp.Dict[str, tp.Any]
Keys = tp.List[str]
MapKeys = tp.Dict[str, Keys]


class OutputsComparator(_ElementWithConditionsComparator):
    """Outputs comparator.
    
    Compare two outputs.
    Conditions are compared.
    """
    
    def __init__(
            self,
            conditions_comparator: IComparator) -> None:
        super().__init__(conditions_comparator=conditions_comparator)
    
    def compare(self, left: Output, right: Output) -> bool:
        """Check if two outputs are equivalent.
        
        :param left: Output.
        :type left: `dict`
        :param right: Other output.
        :type right: `dict`
        :return: Indication if outputs are equivalent.
        :rtype: `bool`
        """
        return self._compare_conditions(left, right)
