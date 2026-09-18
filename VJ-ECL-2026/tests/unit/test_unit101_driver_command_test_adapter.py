"""
\brief UNIT-101(DriverCommandTestAdapter) 단위 테스트 — FN-101, SWD-PH1 §5.8/§9.1.
"""
import unittest

import _bootstrap  # noqa: F401  pylint: disable=unused-import

from src.core.types import Action, Rejection, ReasonCode, Side, Source, ValidCommand
from src.core.command_dispatcher import CommandDispatcher
from src.core.command_validator import CommandValidator
from src.core.facade import EvaluationCycleFacade
from src.core.lock_state_store import LockStateStore
from src.core.policies.driver_command_policy import DriverCommandPolicy
from src.core.policies.ignition_override_policy import IgnitionOverridePolicy
from src.core.policy_chain_executor import PolicyChainExecutor
from src.adapters.pcsil.actuator_output_test_adapter import ActuatorOutputTestAdapter
from src.adapters.pcsil.display_output_test_adapter import DisplayOutputTestAdapter
from src.adapters.pcsil.driver_command_test_adapter import DriverCommandTestAdapter


def _buildFacadeAndDispatcher():
    """UNIT-101 시험용 헬퍼 — 실제 코어로 완전히 배선된 facade/dispatcher를 만든다."""
    store = LockStateStore()
    dispatcher = CommandDispatcher(CommandValidator())
    executor = PolicyChainExecutor(
        store, dispatcher, ActuatorOutputTestAdapter(), DisplayOutputTestAdapter()
    )
    executor.registerPolicy(IgnitionOverridePolicy(store))
    executor.registerPolicy(DriverCommandPolicy(dispatcher, store))
    return EvaluationCycleFacade(dispatcher, executor), dispatcher


class TestDriverCommandTestAdapter(unittest.TestCase):
    """PC/SIL raw_vector(dict) -> DriverCommand 변환 + IF-INT-001 호출을 검증한다."""

    def testSubmitConvertsFullVectorAndForwardsToFacade(self):
        """
        \\brief {"side","action","source"}가 모두 채워진 벡터를 제출하면 그 값 그대로
               DriverCommand로 변환되어 코어에 staging되는지 검증한다. (필드 매핑이
               뒤바뀌면 이 테스트는 실패해야 한다)
        \\technique 실제 컴포넌트 기반 (통합형 단위 테스트, IF-EXT-001 변환 정확성)
        \\testtype 긍정 (Positive)
        \\see UNIT-101 / FN-101, SWR-001/002, SWD-PH1 §9.1
        """
        facade, dispatcher = _buildFacadeAndDispatcher()
        adapter = DriverCommandTestAdapter(facade)
        adapter.submit({"side": "right", "action": "unlock", "source": "mobile_app"})
        self.assertEqual(
            dispatcher.getCurrentCycleCommand(),
            ValidCommand(Side.RIGHT, Action.UNLOCK, Source.MOBILE_APP),
        )

    def testSubmitTreatsMissingKeysAsNoneAndCausesRejection(self):
        """
        \\brief 벡터에 키가 누락되면 None으로 취급되어 하류(CommandValidator)가
               Rejection(INVALID_COMMAND)으로 거절하는지 검증한다. (누락 키가
               예외를 던지거나 기본값으로 통과되면 이 테스트는 실패해야 한다)
        \\technique 오류추정 (필드 누락 — dict.get 방어, SWD-PH1 §10.2)
        \\testtype 부정 (Negative)
        \\see UNIT-101 / FN-101, SWR-001(b), SWD-PH1 §9.1
        """
        facade, dispatcher = _buildFacadeAndDispatcher()
        adapter = DriverCommandTestAdapter(facade)
        adapter.submit({"side": "left"})  # action, source 누락
        self.assertEqual(
            dispatcher.getCurrentCycleCommand(), Rejection(ReasonCode.INVALID_COMMAND)
        )

    def testSubmitDoesNotRaiseForEmptyVector(self):
        """
        \\brief 빈 dict를 제출해도 예외 없이 Rejection으로 귀결되는지 검증한다
               (총함수 계약). (submit이 예외를 던지면 이 테스트는 실패해야 한다)
        \\technique 경계값분석 (완전 누락 — 빈 dict 경계)
        \\testtype 부정 (Negative)
        \\see UNIT-101 / FN-101, SWD-PH1 §5.8 사전조건 없음
        """
        facade, dispatcher = _buildFacadeAndDispatcher()
        adapter = DriverCommandTestAdapter(facade)
        try:
            adapter.submit({})
        except Exception as exc:  # pylint: disable=broad-except
            self.fail(f"submit({{}})이 예외를 던짐: {exc!r}")
        self.assertEqual(
            dispatcher.getCurrentCycleCommand(), Rejection(ReasonCode.INVALID_COMMAND)
        )


if __name__ == "__main__":
    unittest.main()
