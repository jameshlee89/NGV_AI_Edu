"""
\brief UNIT-001(EvaluationCycleFacade) 단위 테스트 — FN-001/002, SWD-PH1 §5.7.
"""
import unittest

import _bootstrap  # noqa: F401  pylint: disable=unused-import

from src.core.types import (
    Action,
    CycleStatus,
    DriverCommand,
    LockState,
    Side,
    Source,
    ValidCommand,
    VehicleSnapshot,
)
from src.core.command_dispatcher import CommandDispatcher
from src.core.command_validator import CommandValidator
from src.core.facade import EvaluationCycleFacade
from src.core.lock_state_store import LockStateStore
from src.core.policies.driver_command_policy import DriverCommandPolicy
from src.core.policies.ignition_override_policy import IgnitionOverridePolicy
from src.core.policy_chain_executor import PolicyChainExecutor
from src.adapters.pcsil.actuator_output_test_adapter import ActuatorOutputTestAdapter
from src.adapters.pcsil.display_output_test_adapter import DisplayOutputTestAdapter


def _buildFacade():
    """실제 UNIT-002~007로 완전히 배선된 EvaluationCycleFacade를 만드는 테스트 헬퍼."""
    store = LockStateStore()
    dispatcher = CommandDispatcher(CommandValidator())
    actuator = ActuatorOutputTestAdapter()
    display = DisplayOutputTestAdapter()
    executor = PolicyChainExecutor(store, dispatcher, actuator, display)
    executor.registerPolicy(IgnitionOverridePolicy(store))
    executor.registerPolicy(DriverCommandPolicy(dispatcher, store))
    facade = EvaluationCycleFacade(dispatcher, executor)
    return facade, dispatcher, store


class TestEvaluationCycleFacade(unittest.TestCase):
    """submitDriverCommand/submitVehicleSnapshot 위임 동작을 검증한다 (IF-INT-001/002)."""

    def testSubmitDriverCommandDelegatesToDispatcher(self):
        """
        \\brief submitDriverCommand()가 CommandDispatcher.dispatch()에 그대로
               위임되어 이후 평가주기에서 명령이 반영되는지 검증한다. (위임이
               제거되면 이 테스트는 실패해야 한다)
        \\technique 실제 컴포넌트 기반 (통합형 단위 테스트, IF-INT-001)
        \\testtype 긍정 (Positive)
        \\see UNIT-001 / FN-001, SWR-001/002
        """
        facade, _, _ = _buildFacade()
        facade.submitDriverCommand(DriverCommand(side="left", action="lock", source="avn"))
        result = facade.submitVehicleSnapshot(VehicleSnapshot(timestampS=0.0, ignitionOn=True))
        self.assertEqual(result.status, CycleStatus.COMMITTED)
        self.assertEqual(result.lockLeft, LockState.LOCK)

    def testSubmitVehicleSnapshotDelegatesToExecutorAndReturnsResult(self):
        """
        \\brief submitVehicleSnapshot()이 PolicyChainExecutor.evaluate()에 위임되고
               그 반환값을 그대로 돌려주는지 검증한다. (위임 결과가 가공되거나
               삭제되면 이 테스트는 실패해야 한다)
        \\technique 실제 컴포넌트 기반 (통합형 단위 테스트, IF-INT-002/009)
        \\testtype 긍정 (Positive)
        \\see UNIT-001 / FN-002, SWR-004/020
        """
        facade, _, store = _buildFacade()
        result = facade.submitVehicleSnapshot(VehicleSnapshot(timestampS=1.0, ignitionOn=False))
        self.assertEqual(result.status, CycleStatus.COMMITTED)
        self.assertEqual(result.lockLeft, LockState.RELEASE)
        self.assertEqual(store.readCurrent().left, LockState.RELEASE)


if __name__ == "__main__":
    unittest.main()
