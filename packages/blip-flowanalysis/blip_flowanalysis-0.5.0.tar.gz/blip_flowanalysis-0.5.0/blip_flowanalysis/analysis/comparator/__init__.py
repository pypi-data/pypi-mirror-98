"""Comparators for chatbot entities.

Contains comparators for some entities on chatbot.
Each comparator is an instance with `compare` method.
This method compares two objects and indicates if they are equivalent.

Classes:
  * Conditions comparator.
  * Outputs comparator.
  * Actions comparator.
  * States comparator.
"""

from __future__ import annotations

__author__ = 'Gabriel Salgado'
__version__ = '0.1.0'
__all__ = [
    'ConditionsComparator',
    'OutputsComparator',
    'ActionsComparator',
    'StatesComparator',
]

from .conditions_comparator import ConditionsComparator
from .outputs_comparator import OutputsComparator
from .actions_comparator import ActionsComparator
from .states_comparator import StatesComparator
