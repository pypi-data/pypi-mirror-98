__author__ = 'Gabriel Salgado'
__version__ = '0.1.0'
import abc
import typing as tp

Data = tp.Dict[str, tp.Any]


class IComparator(abc.ABC):
    """Interface for comparators."""
    
    def __init__(self) -> None:
        super().__init__()
    
    @abc.abstractmethod
    def compare(self, left: Data, right: Data) -> bool:
        """Check if two data on bot settings are equivalent.
        
        :param left: Data.
        :type left: `dict`
        :param right: Other data.
        :type right: `dict`
        :return: Indication if data are equivalent.
        :rtype: `bool`
        """
        raise NotImplementedError()
