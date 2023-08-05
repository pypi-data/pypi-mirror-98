__author__ = 'Gabriel Salgado'
import typing as tp
from unittest import mock as mk

import pytest
import pytest_mock as pm

from blip_flowanalysis.analysis.comparator.\
    interface_comparator import IComparator
from blip_flowanalysis.analysis.comparator.\
    actions_comparator import ActionsComparator

Keys = tp.List[str]
Values = tp.List[tp.Any]
MapKeys = tp.Dict[str, Keys]
Dict = tp.Dict[str, tp.Any]


class TestActionsComparator(object):
    
    @pytest.fixture
    def type(self) -> str:
        return 'type'
    
    @pytest.fixture
    def keys(self) -> Keys:
        return [
            'key_1',
            'key_2',
            'key_3',
        ]
    
    @pytest.fixture
    def map_keys(self, type: str, keys: Keys) -> MapKeys:
        return {type: keys}
    
    @pytest.fixture
    def left_settings(self, mocker: pm.MockFixture) -> mk.Mock:
        return mocker.Mock()
    
    @pytest.fixture
    def right_settings(self, mocker: pm.MockFixture) -> mk.Mock:
        return mocker.Mock()
    
    @pytest.fixture
    def left(self, type: str, left_settings: mk.Mock) -> Dict:
        return {
            'type': type,
            'settings': left_settings,
        }
    
    @pytest.fixture
    def right(self, type: str, right_settings: mk.Mock) -> Dict:
        return {
            'type': type,
            'settings': right_settings,
        }
    
    @pytest.fixture
    def conditions_comparator(self, mocker: pm.MockFixture) -> IComparator:
        return mocker.Mock(spec=IComparator)
    
    @pytest.fixture
    def actions_comparator(
            self,
            map_keys: MapKeys,
            conditions_comparator: IComparator) -> ActionsComparator:
        return ActionsComparator(conditions_comparator, map_keys)
    
    def test__actions_comparator(
            self,
            map_keys: MapKeys,
            conditions_comparator: IComparator,
            actions_comparator: ActionsComparator) -> None:
        assert actions_comparator.map_keys == map_keys
        assert actions_comparator.conditions_comparator\
            is conditions_comparator
    
    def test__compare__all_equal(
            self,
            mocker: pm.MockFixture,
            left: Dict, right: Dict,
            left_settings: mk.Mock, right_settings: mk.Mock, keys: Keys,
            actions_comparator: ActionsComparator) -> None:
        equal_dicts = True
        equal_conditions = True
        expected = True
        compare_dicts = mocker.Mock(return_value=equal_dicts)
        compare_conditions = mocker.Mock(return_value=equal_conditions)
        actions_comparator._compare_dicts = compare_dicts
        actions_comparator._compare_conditions = compare_conditions
        result = actions_comparator.compare(left, right)
        assert result is expected
        compare_dicts.assert_called_once_with(
            left_settings, right_settings, keys)
        compare_conditions.assert_called_once_with(left, right)
    
    def test__compare__different_conditions(
            self,
            mocker: pm.MockFixture,
            left: Dict, right: Dict,
            left_settings: mk.Mock, right_settings: mk.Mock, keys: Keys,
            actions_comparator: ActionsComparator) -> None:
        equal_dicts = True
        equal_conditions = False
        expected = False
        compare_dicts = mocker.Mock(return_value=equal_dicts)
        compare_conditions = mocker.Mock(return_value=equal_conditions)
        actions_comparator._compare_dicts = compare_dicts
        actions_comparator._compare_conditions = compare_conditions
        result = actions_comparator.compare(left, right)
        assert result is expected
        compare_conditions.assert_called_once_with(left, right)
    
    def test__compare__different_settings(
            self,
            mocker: pm.MockFixture,
            left: Dict, right: Dict,
            left_settings: mk.Mock, right_settings: mk.Mock, keys: Keys,
            actions_comparator: ActionsComparator) -> None:
        equal_dicts = False
        equal_conditions = True
        expected = False
        compare_dicts = mocker.Mock(return_value=equal_dicts)
        compare_conditions = mocker.Mock(return_value=equal_conditions)
        actions_comparator._compare_dicts = compare_dicts
        actions_comparator._compare_conditions = compare_conditions
        result = actions_comparator.compare(left, right)
        assert result is expected
        compare_dicts.assert_called_once_with(
            left_settings, right_settings, keys)
    
    def test__compare__different_types(
            self,
            mocker: pm.MockFixture,
            left: Dict, right: Dict,
            type: str,
            actions_comparator: ActionsComparator) -> None:
        expected = False
        right['type'] = f'other_{type}'
        compare_dicts = mocker.Mock()
        compare_conditions = mocker.Mock()
        actions_comparator._compare_dicts = compare_dicts
        actions_comparator._compare_conditions = compare_conditions
        result = actions_comparator.compare(left, right)
        assert result is expected
        compare_dicts.assert_not_called()
        compare_conditions.assert_not_called()
