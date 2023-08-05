__author__ = 'Gabriel Salgado'
import typing as tp
from unittest import mock as mk

import pytest
import pytest_mock as pm

from blip_flowanalysis.analysis.comparator.\
    interface_comparator import IComparator
from blip_flowanalysis.analysis.comparator.\
    outputs_comparator import OutputsComparator


class TestOutputsComparator(object):
    
    @pytest.fixture
    def conditions_comparator(self, mocker: pm.MockFixture) -> IComparator:
        return mocker.Mock(spec=IComparator)
    
    @pytest.fixture
    def outputs_comparator(
            self,
            conditions_comparator: IComparator) -> OutputsComparator:
        return OutputsComparator(conditions_comparator)
    
    def test__outputs_comparator(
            self,
            conditions_comparator: IComparator,
            outputs_comparator: OutputsComparator) -> None:
        assert outputs_comparator.conditions_comparator\
            is conditions_comparator
    
    def test__compare(
            self,
            mocker: pm.MockFixture,
            outputs_comparator: OutputsComparator) -> None:
        expected = mocker.Mock(spec=bool)
        left = mocker.Mock()
        right = mocker.Mock()
        compare_conditions = mocker.Mock(return_value=expected)
        outputs_comparator._compare_conditions = compare_conditions
        result = outputs_comparator.compare(left, right)
        assert result is expected
        compare_conditions.assert_called_once_with(left, right)
