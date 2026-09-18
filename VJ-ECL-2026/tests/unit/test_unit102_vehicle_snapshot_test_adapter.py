"""
\brief UNIT-102(VehicleSnapshotTestAdapter) 단위 테스트 — FN-102, SWD-PH1 §5.8/§9.1.
"""
import unittest

import _bootstrap  # noqa: F401  pylint: disable=unused-import

from src.core.types import CycleStatus, LockState, VehicleSnapshot
from src.core.command_dispatcher import CommandDispatcher
from src.core.command_validator import CommandValidator
from src.core.facade import EvaluationCycleFacade
from src.core.lock_state_store import LockStateStore
from src.core.policies.driver_command_policy import DriverCommandPolicy
from src.core.policies.ignition_override_policy import IgnitionOverridePolicy
from src.core.policy_chain_executor import PolicyChainExecutor
from src.adapters.pcsil.actuator_output_test_adapter import ActuatorOutputTestAdapter
from src.adapters.pcsil.display_output_test_adapter import DisplayOutputTestAdapter
from src.adapters.pcsil.vehicle_snapshot_test_adapter import VehicleSnapshotTestAdapter


class _CapturingFacade:
    """테스트 전용 스텁 — submitVehicleSnapshot 인자를 그대로 캡처만 한다."""

    def __init__(self):
        self.lastSnapshot = None

    def submitVehicleSnapshot(self, snapshot: VehicleSnapshot):
        self.lastSnapshot = snapshot
        return None


def _buildFacade():
    """UNIT-102 시험용 헬퍼 — 실제 코어로 완전히 배선된 facade를 만든다."""
    store = LockStateStore()
    dispatcher = CommandDispatcher(CommandValidator())
    executor = PolicyChainExecutor(
        store, dispatcher, ActuatorOutputTestAdapter(), DisplayOutputTestAdapter()
    )
    executor.registerPolicy(IgnitionOverridePolicy(store))
    executor.registerPolicy(DriverCommandPolicy(dispatcher, store))
    return EvaluationCycleFacade(dispatcher, executor)


class TestVehicleSnapshotTestAdapter(unittest.TestCase):
    """PC/SIL raw_vector(dict) -> VehicleSnapshot 변환 + IF-INT-002 호출을 검증한다."""

    def testSubmitConvertsValidVectorAndReturnsEvaluationResult(self):
        """
        \\brief ignition_on=True인 유효 벡터를 제출하면 평가주기가 실행되어
               EvaluationResult(status=COMMITTED)를 반환하는지 검증한다. (변환/위임이
               깨지면 이 테스트는 실패해야 한다)
        \\technique 실제 컴포넌트 기반 (통합형 단위 테스트, IF-EXT-002 변환 정확성)
        \\testtype 긍정 (Positive)
        \\see UNIT-102 / FN-102, SWR-020, SWD-PH1 §9.1
        """
        adapter = VehicleSnapshotTestAdapter(_buildFacade())
        result = adapter.submit({"timestamp_s": 1.5, "ignition_on": True})
        self.assertEqual(result.status, CycleStatus.COMMITTED)

    def testSubmitTreatsMissingIgnitionOnAsInvalidAndForcesRelease(self):
        """
        \\brief ignition_on 키가 누락되면 None으로 전달되어 IgnitionOverridePolicy가
               INVALID(=FALSE와 동일)로 처리해 RELEASE를 강제하는지 검증한다.
               (누락을 True/False로 오판하면 이 테스트는 실패해야 한다)
        \\technique 오류추정 (필드 누락 — SWR-020(b) 안전측 처리)
        \\testtype 부정 (Negative)
        \\see UNIT-102 / FN-102, SWR-020(b)
        """
        adapter = VehicleSnapshotTestAdapter(_buildFacade())
        result = adapter.submit({"timestamp_s": 0.0})
        self.assertEqual(result.lockLeft, LockState.RELEASE)
        self.assertEqual(result.lockRight, LockState.RELEASE)

    def testSubmitDefaultsMissingTimestampToZeroWithWarning(self):
        """
        \\brief timestamp_s 키가 누락되면 0.0으로 대체되고 WARNING 로그가 남는지
               검증한다(스냅샷 전체를 무효화하지 않음, SWD-PH1 §10.2). (누락 시
               예외가 발생하거나 경고가 없으면 이 테스트는 실패해야 한다)
        \\technique 오류추정 (필드 누락 — 방어적 완화)
        \\testtype 부정 (Negative)
        \\see UNIT-102 / FN-102, SWD-PH1 §10.2
        """
        adapter = VehicleSnapshotTestAdapter(_buildFacade())
        with self.assertLogs("vjecl.adapters.pcsil.vehicle_snapshot", level="WARNING"):
            result = adapter.submit({"ignition_on": True})
        self.assertEqual(result.status, CycleStatus.COMMITTED)

    def testSubmitDefaultsMalformedTimestampToZeroWithWarning(self):
        """
        \\brief timestamp_s가 숫자로 변환 불가능한 문자열이면 0.0으로 대체되고
               WARNING 로그가 남는지 검증한다(예외 없음). (형식 오류가 예외를
               던지면 이 테스트는 실패해야 한다)
        \\technique 경계값분석 (형식 오류 입력 경계)
        \\testtype 부정 (Negative)
        \\see UNIT-102 / FN-102, SWD-PH1 §10.2
        """
        adapter = VehicleSnapshotTestAdapter(_buildFacade())
        with self.assertLogs("vjecl.adapters.pcsil.vehicle_snapshot", level="WARNING"):
            try:
                adapter.submit({"timestamp_s": "not-a-number", "ignition_on": True})
            except Exception as exc:  # pylint: disable=broad-except
                self.fail(f"submit()이 예외를 던짐: {exc!r}")

    def testSubmitParsesNumericStringTimestamp(self):
        """
        \\brief timestamp_s가 숫자 형식 문자열("2.5")이면 float 2.5로 정상 변환되는지
               검증한다(§9.1 "float|str" 계약). (문자열 숫자를 거절하면 이 테스트는
               실패해야 한다)
        \\technique 동등분할 (유효 문자열 숫자 클래스)
        \\testtype 긍정 (Positive)
        \\see UNIT-102 / FN-102, SWD-PH1 §9.1
        """
        facade = _CapturingFacade()
        adapter = VehicleSnapshotTestAdapter(facade)
        adapter.submit({"timestamp_s": "2.5", "ignition_on": True})
        self.assertEqual(facade.lastSnapshot, VehicleSnapshot(timestampS=2.5, ignitionOn=True))


if __name__ == "__main__":
    unittest.main()
