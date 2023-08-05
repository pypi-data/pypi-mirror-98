"""This module contains implementations for abstract.Analyser class.

Classes:
  * MissingTrackings - Verify if flow has minimum Tracking amount.
  * ProcessHTTPReturnValidation - Verify if HTTP calls returns in the flow are validated.
  * LongScript - Check if bot scripts are too long.
  * DuplicatedPaths - Check if bot flow contains duplicated paths.
"""

from __future__ import annotations

__all__ = [
    "MissingTrackings",
    "ProcessHTTPReturnValidation",
    "LongScript",
    "DuplicatedPaths",
]

from .missing_trackings import MissingTrackings
from .process_http_return_validation import ProcessHTTPReturnValidation
from .long_script import LongScript
from .duplicated_paths import DuplicatedPaths
