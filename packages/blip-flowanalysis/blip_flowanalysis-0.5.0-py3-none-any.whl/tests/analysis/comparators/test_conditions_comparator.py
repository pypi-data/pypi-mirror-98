__author__ = 'Gabriel Salgado'
import typing as tp

import pytest
import pytest_mock as pm

from blip_flowanalysis.analysis.comparator.\
    conditions_comparator import ConditionsComparator

Keys = tp.List[str]


class TestConditionsComparator(object):
    
    @pytest.fixture
    def keys(self) -> Keys:
        return [
            'key_1',
            'key_2',
            'key_3',
        ]
    
    @pytest.fixture
    def conditions_comparator(
            self,
            keys: Keys) -> ConditionsComparator:
        return ConditionsComparator(keys)
    
    def test__conditions_comparator(
            self,
            conditions_comparator: ConditionsComparator,
            keys: Keys) -> None:
        assert conditions_comparator.keys is keys
    
    def test__compare(
            self,
            mocker: pm.MockFixture,
            conditions_comparator: ConditionsComparator,
            keys: Keys) -> None:
        expected = mocker.Mock(spec=bool)
        left = mocker.Mock()
        right = mocker.Mock()
        compare_dicts = mocker.Mock(return_value=expected)
        conditions_comparator._compare_dicts = compare_dicts
        result = conditions_comparator.compare(left, right)
        assert result is expected
        compare_dicts.assert_called_once_with(left, right, keys)
