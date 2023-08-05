__author__ = 'Gabriel Salgado'
import typing as tp
from unittest import mock as mk

import pytest
import pytest_mock as pm

from blip_flowanalysis.analysis.comparator.\
    interface_comparator import IComparator
from blip_flowanalysis.analysis.comparator\
    import _specific_comparators  # noqa

_ElementWithConditionsComparator =\
    _specific_comparators._ElementWithConditionsComparator  # noqa
_DictComparator = _specific_comparators._DictComparator  # noqa
Mocks = tp.List[mk.Mock]


class TestDictComparator(object):
    
    @pytest.fixture
    def keys(self) -> tp.List[str]:
        return [
            'key_1',
            'key_2',
            'key_3',
        ]
    
    @pytest.fixture
    def other_keys(self) -> tp.List[str]:
        return [
            'other_key_1',
            'other_key_2',
            'other_key_3',
        ]
    
    @pytest.fixture
    def values(self, keys: tp.List[str]) -> tp.List[tp.Any]:
        return list(range(len(keys)))
    
    @pytest.fixture
    def other_values(self, other_keys: tp.List[str]) -> tp.List[tp.Any]:
        offset = 1
        return list(range(offset, len(other_keys) + offset))
    
    @pytest.fixture
    def dict_comparator(self) -> _DictComparator:
        
        class Comparator(_DictComparator):
            def compare(self, _, __) -> bool:
                return False
        
        return Comparator()
    
    def test__compare__all_equal(
            self,
            dict_comparator: _DictComparator,
            keys: tp.List[str], values: tp.List[tp.Any]) -> None:
        left = dict(zip(keys, values))
        right = dict(zip(keys, values))
        assert dict_comparator._compare_dicts(left, right, keys)
        assert dict_comparator._compare_dicts(right, left, keys)
    
    def test__compare__empty(
            self,
            dict_comparator: _DictComparator) -> None:
        left = dict()
        right = dict()
        assert dict_comparator._compare_dicts(left, right, list())
        assert dict_comparator._compare_dicts(right, left, list())
    
    def test__compare__other_is_empty(
            self,
            dict_comparator: _DictComparator,
            keys: tp.List[str], values: tp.List[tp.Any]) -> None:
        left = dict(zip(keys, values))
        right = dict()
        assert not dict_comparator._compare_dicts(left, right, keys)
        assert not dict_comparator._compare_dicts(right, left, keys)
    
    def test__compare__other_values_on_other(
            self,
            dict_comparator: _DictComparator,
            keys: tp.List[str],
            values: tp.List[tp.Any],
            other_values: tp.List[tp.Any]) -> None:
        left = dict(zip(keys, values))
        right = dict(zip(keys, other_values))
        assert not dict_comparator._compare_dicts(left, right, keys)
        assert not dict_comparator._compare_dicts(right, left, keys)
    
    def test__compare__absent_on_other(
            self,
            dict_comparator: _DictComparator,
            keys: tp.List[str], values: tp.List[tp.Any]) -> None:
        left = dict(zip(keys, values))
        right = dict(zip(keys, values))
        del right[keys[0]]
        assert not dict_comparator._compare_dicts(left, right, keys)
        assert not dict_comparator._compare_dicts(right, left, keys)
    
    def test__compare__other_keys_on_other(
            self,
            dict_comparator: _DictComparator,
            keys: tp.List[str],
            other_keys: tp.List[str],
            values: tp.List[tp.Any]) -> None:
        left = dict(zip(keys, values))
        right = dict(zip(other_keys, values))
        assert not dict_comparator._compare_dicts(left, right, keys)
        assert not dict_comparator._compare_dicts(right, left, keys)


class TestElementWithConditionsComparator(object):
    
    @pytest.fixture
    def left_conditions(self, mocker: pm.MockFixture) -> Mocks:
        return [
            mocker.Mock(),
            mocker.Mock(),
            mocker.Mock(),
        ]
    
    @pytest.fixture
    def right_conditions(self, mocker: pm.MockFixture) -> Mocks:
        return [
            mocker.Mock(),
            mocker.Mock(),
            mocker.Mock(),
        ]
    
    @pytest.fixture
    def left(self, left_conditions: Mocks) -> tp.Dict[str, Mocks]:
        return {
            'conditions': left_conditions,
        }
    
    @pytest.fixture
    def right(self, right_conditions: Mocks) -> tp.Dict[str, Mocks]:
        return {
            'conditions': right_conditions,
        }
    
    @pytest.fixture
    def conditions_comparator(self, mocker: pm.MockFixture) -> IComparator:
        conditions_comparator = mocker.Mock(spec=IComparator)
        conditions_comparator.compare = mocker.Mock()
        return conditions_comparator
    
    @pytest.fixture
    def comparator(
            self,
            conditions_comparator: IComparator
    ) -> _ElementWithConditionsComparator:
        
        class Comparator(_ElementWithConditionsComparator):
            def compare(self, _, __) -> bool:
                return False
        
        return Comparator(conditions_comparator)
    
    def test__element_with_conditions_comparator(
            self,
            conditions_comparator: IComparator,
            comparator: _ElementWithConditionsComparator) -> None:
        assert comparator.conditions_comparator is conditions_comparator
    
    def test__compare_conditions__all_equal(
            self,
            mocker: pm.MockFixture,
            left_conditions: Mocks,
            right_conditions: Mocks,
            left: tp.Dict[str, Mocks],
            right: tp.Dict[str, Mocks],
            conditions_comparator: mk.Mock,
            comparator: _ElementWithConditionsComparator) -> None:
        side_effect = [True for _ in left['conditions']]
        conditions_comparator.compare.side_effect = side_effect
        assert comparator._compare_conditions(left, right)
        conditions_comparator.compare.assert_has_calls([
            mocker.call(l, r)
            for l, r in zip(left_conditions, right_conditions)
        ])
    
    @pytest.mark.parametrize('n_diff', [0, 1, 2])
    def test__compare__one_different(
            self,
            n_diff: int,
            mocker: pm.MockFixture,
            left_conditions: Mocks,
            right_conditions: Mocks,
            left: tp.Dict[str, Mocks],
            right: tp.Dict[str, Mocks],
            conditions_comparator: mk.Mock,
            comparator: _ElementWithConditionsComparator) -> None:
        n_lim = n_diff + 1
        side_effect = [True for _ in left['conditions']]
        side_effect[n_diff] = False
        conditions_comparator.compare.side_effect = side_effect
        assert not comparator._compare_conditions(left, right)
        conditions_comparator.compare.assert_has_calls([
            mocker.call(l, r)
            for l, r in zip(left_conditions[:n_lim], right_conditions[:n_lim])
        ])
    
    def test__compare__all_different(
            self,
            left_conditions: Mocks,
            right_conditions: Mocks,
            left: tp.Dict[str, Mocks],
            right: tp.Dict[str, Mocks],
            conditions_comparator: mk.Mock,
            comparator: _ElementWithConditionsComparator) -> None:
        side_effect = [False for _ in left['conditions']]
        conditions_comparator.compare.side_effect = side_effect
        assert not comparator._compare_conditions(left, right)
        conditions_comparator.compare.assert_called_once_with(
            left_conditions[0], right_conditions[0]
        )
    
    def test__compare__different_size(
            self,
            right_conditions: Mocks,
            left: tp.Dict[str, Mocks],
            right: tp.Dict[str, Mocks],
            conditions_comparator: mk.Mock,
            comparator: _ElementWithConditionsComparator) -> None:
        right['conditions'] = right_conditions[:-1]
        assert not comparator._compare_conditions(left, right)
        conditions_comparator.compare.assert_not_called()
    
    def test__compare__other_is_empty(
            self,
            left: tp.Dict[str, Mocks],
            right: tp.Dict[str, Mocks],
            conditions_comparator: mk.Mock,
            comparator: _ElementWithConditionsComparator) -> None:
        right['conditions'] = list()
        assert not comparator._compare_conditions(left, right)
        conditions_comparator.compare.assert_not_called()
    
    def test__compare__both_are_empty(
            self,
            left: tp.Dict[str, Mocks],
            right: tp.Dict[str, Mocks],
            conditions_comparator: mk.Mock,
            comparator: _ElementWithConditionsComparator) -> None:
        left['conditions'] = list()
        right['conditions'] = list()
        assert comparator._compare_conditions(left, right)
        conditions_comparator.compare.assert_not_called()
