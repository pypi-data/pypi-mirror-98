__author__ = 'Gabriel Salgado'
import typing as tp
from unittest import mock as mk

import pytest
import pytest_mock as pm

from blip_flowanalysis.analysis.comparator.\
    interface_comparator import IComparator
from blip_flowanalysis.analysis.comparator.\
    states_comparator import StatesComparator

State = tp.Dict[str, tp.Any]
Output = tp.Dict[str, tp.Any]
Outputs = tp.List[Output]
Action = tp.Dict[str, tp.Any]
Actions = tp.List[Action]


class TestStatesComparator(object):
    
    @pytest.fixture
    def outputs_comparator(self, mocker: pm.MockFixture) -> mk.Mock:
        return mocker.Mock()
    
    @pytest.fixture
    def actions_comparator(self, mocker: pm.MockFixture) -> mk.Mock:
        return mocker.Mock()
    
    @pytest.fixture
    def outputs_key(self) -> str:
        return 'outputs_key'
    
    @pytest.fixture
    def actions_io(self) -> tuple:
        return 'actions_1', 'actions_2'
    
    @pytest.fixture
    def left_outputs(self, mocker: pm.MockFixture) -> Outputs:
        return [
            mocker.Mock(),
            mocker.Mock(),
            mocker.Mock(),
        ]
    
    @pytest.fixture
    def right_outputs(self, mocker: pm.MockFixture) -> Outputs:
        return [
            mocker.Mock(),
            mocker.Mock(),
            mocker.Mock(),
        ]
    
    @pytest.fixture
    def left_actions(self, mocker: pm.MockFixture) -> Outputs:
        return [
            mocker.Mock(),
            mocker.Mock(),
            mocker.Mock(),
        ]
    
    @pytest.fixture
    def right_actions(self, mocker: pm.MockFixture) -> Outputs:
        return [
            mocker.Mock(),
            mocker.Mock(),
            mocker.Mock(),
        ]
    
    @pytest.fixture
    def left(
            self,
            mocker: pm.MockFixture,
            outputs_key: str,
            actions_io: tuple) -> State:
        left = dict()
        left[outputs_key] = mocker.Mock()
        for action_interface in actions_io:
            left[action_interface] = mocker.Mock()
        return left
    
    @pytest.fixture
    def right(
            self,
            mocker: pm.MockFixture,
            outputs_key: str,
            actions_io: tuple) -> State:
        right = dict()
        right[outputs_key] = mocker.Mock()
        for action_interface in actions_io:
            right[action_interface] = mocker.Mock()
        return right
    
    @pytest.fixture
    def states_comparator(
            self,
            outputs_comparator: IComparator,
            actions_comparator: IComparator,
            outputs_key: str,
            actions_io: tuple) -> StatesComparator:
        return StatesComparator(
            outputs_comparator,
            actions_comparator,
            outputs_key,
            actions_io)
    
    def test__states_comparator(
            self,
            outputs_comparator: mk.Mock,
            actions_comparator: mk.Mock,
            outputs_key: str,
            actions_io: tuple,
            states_comparator: StatesComparator) -> None:
        assert states_comparator.outputs_comparator is outputs_comparator
        assert states_comparator.actions_comparator is actions_comparator
        assert states_comparator.outputs_key is outputs_key
        assert states_comparator.actions_io is actions_io
    
    def test__compare_outputs__all_equal(
            self,
            mocker: pm.MockFixture,
            outputs_comparator: mk.Mock,
            left_outputs: Outputs, right_outputs: Outputs,
            states_comparator: StatesComparator) -> None:
        side_effect = [True for _ in left_outputs]
        expected = True
        left, right = left_outputs, right_outputs
        compare = mocker.Mock(side_effect=side_effect)
        outputs_comparator.compare = compare
        result = states_comparator._compare_outputs(left, right)
        assert result is expected
        compare.assert_has_calls([
            mocker.call(l, r)
            for l, r in zip(left, right)
        ])
    
    def test__compare_outputs__one_different(
            self,
            mocker: pm.MockFixture,
            outputs_comparator: mk.Mock,
            left_outputs: Outputs, right_outputs: Outputs,
            states_comparator: StatesComparator) -> None:
        n_diff = 1
        n_lim = n_diff + 1
        side_effect = [True for _ in left_outputs]
        side_effect[n_diff] = False
        expected = False
        left, right = left_outputs, right_outputs
        compare = mocker.Mock(side_effect=side_effect)
        outputs_comparator.compare = compare
        result = states_comparator._compare_outputs(left, right)
        assert result is expected
        compare.assert_has_calls([
            mocker.call(l, r)
            for l, r in zip(left[:n_lim], right[:n_lim])
        ])
    
    def test__compare_outputs__different_size(
            self,
            mocker: pm.MockFixture,
            outputs_comparator: mk.Mock,
            left_outputs: Outputs, right_outputs: Outputs,
            states_comparator: StatesComparator) -> None:
        expected = False
        left, right = left_outputs, right_outputs[:-1]
        compare = mocker.Mock()
        outputs_comparator.compare = compare
        result = states_comparator._compare_outputs(left, right)
        assert result is expected
        compare.assert_not_called()
    
    def test__compare_actions__all_equal(
            self,
            mocker: pm.MockFixture,
            actions_comparator: mk.Mock,
            left_actions: Actions, right_actions: Actions,
            states_comparator: StatesComparator) -> None:
        side_effect = [True for _ in left_actions]
        expected = True
        left, right = left_actions, right_actions
        compare = mocker.Mock(side_effect=side_effect)
        actions_comparator.compare = compare
        result = states_comparator._compare_actions(left, right)
        assert result is expected
        compare.assert_has_calls([
            mocker.call(l, r)
            for l, r in zip(left, right)
        ])
    
    def test__compare_actions__one_different(
            self,
            mocker: pm.MockFixture,
            actions_comparator: mk.Mock,
            left_actions: Actions, right_actions: Actions,
            states_comparator: StatesComparator) -> None:
        n_diff = 1
        n_lim = n_diff + 1
        side_effect = [True for _ in left_actions]
        side_effect[n_diff] = False
        expected = False
        left, right = left_actions, right_actions
        compare = mocker.Mock(side_effect=side_effect)
        actions_comparator.compare = compare
        result = states_comparator._compare_actions(left, right)
        assert result is expected
        compare.assert_has_calls([
            mocker.call(l, r)
            for l, r in zip(left[:n_lim], right[:n_lim])
        ])
    
    def test__compare_actions__different_size(
            self,
            mocker: pm.MockFixture,
            actions_comparator: mk.Mock,
            left_actions: Actions, right_actions: Actions,
            states_comparator: StatesComparator) -> None:
        expected = False
        left, right = left_actions, right_actions[:-1]
        compare = mocker.Mock()
        actions_comparator.compare = compare
        result = states_comparator._compare_actions(left, right)
        assert result is expected
        compare.assert_not_called()
    
    def test__compare__all_equal(
            self,
            mocker: pm.MockFixture,
            outputs_key: str, actions_io: tuple,
            left: State, right: State,
            states_comparator: StatesComparator) -> None:
        equal_outputs = True
        equal_actions = [True for _ in actions_io]
        expected = True
        compare_outputs = mocker.Mock(return_value=equal_outputs)
        compare_actions = mocker.Mock(side_effect=equal_actions)
        states_comparator._compare_outputs = compare_outputs
        states_comparator._compare_actions = compare_actions
        result = states_comparator.compare(left, right)
        assert result is expected
        compare_outputs.assert_called_once_with(
            left[outputs_key], right[outputs_key])
        compare_actions.assert_has_calls([
            mocker.call(left[action_interface], right[action_interface])
            for action_interface in actions_io
        ])
    
    def test__compare__one_different_actions_list(
            self,
            mocker: pm.MockFixture,
            actions_io: tuple,
            left: State, right: State,
            states_comparator: StatesComparator) -> None:
        n_diff = 1
        n_lim = n_diff + 1
        equal_outputs = True
        equal_actions = [True for _ in actions_io]
        equal_actions[n_diff] = False
        expected = False
        compare_outputs = mocker.Mock(return_value=equal_outputs)
        compare_actions = mocker.Mock(side_effect=equal_actions)
        states_comparator._compare_outputs = compare_outputs
        states_comparator._compare_actions = compare_actions
        result = states_comparator.compare(left, right)
        assert result is expected
        compare_actions.assert_has_calls([
            mocker.call(left[action_interface], right[action_interface])
            for action_interface in actions_io[:n_lim]
        ])
    
    def test__compare__different_outputs_list(
            self,
            mocker: pm.MockFixture,
            outputs_key: str, actions_io: tuple,
            left: State, right: State,
            states_comparator: StatesComparator) -> None:
        equal_outputs = False
        equal_actions = [True for _ in actions_io]
        expected = False
        compare_outputs = mocker.Mock(return_value=equal_outputs)
        compare_actions = mocker.Mock(side_effect=equal_actions)
        states_comparator._compare_outputs = compare_outputs
        states_comparator._compare_actions = compare_actions
        result = states_comparator.compare(left, right)
        assert result is expected
        compare_outputs.assert_called_once_with(
            left[outputs_key], right[outputs_key])
