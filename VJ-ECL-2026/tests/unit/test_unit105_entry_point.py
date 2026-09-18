"""
\brief UNIT-105(PcSilHarnessEntryPoint) 단위 테스트 — FN-105, SWD-PH1 §5.9.
"""
import unittest

import _bootstrap  # noqa: F401  pylint: disable=unused-import

from src.core.types import DisplayState, LockState, ReasonCode
from src.adapters.pcsil.entry_point import buildSystem


class TestBuildSystem(unittest.TestCase):
    """buildSystem()이 반환한 SystemHandle의 배선이 실제로 동작하는지 검증한다."""

    def testWiresNominalDriverCommandThroughToOutputs(self):
        """
        \\brief driverAdapter.submit + vehicleAdapter.submit(ignition_on=True)로 좌측
               잠금을 지시하면 actuatorAdapter/displayAdapter가 그 결과를 반영하는지
               검증한다(전체 배선이 끊기면 이 테스트는 실패해야 한다).
        \\technique 실제 컴포넌트 기반 (통합형 단위 테스트, 조립 계약 검증)
        \\testtype 긍정 (Positive)
        \\see UNIT-105 / FN-105, SWD-PH1 §5.9 사후조건
        """
        handle = buildSystem()
        handle.driverAdapter.submit({"side": "left", "action": "lock", "source": "avn"})
        handle.vehicleAdapter.submit({"timestamp_s": 0.0, "ignition_on": True})

        self.assertEqual(
            handle.actuatorAdapter.getLastApplied().left, LockState.LOCK
        )
        self.assertEqual(
            handle.displayAdapter.getLastShown(), (DisplayState.LOCKED_LEFT, ReasonCode.NONE)
        )

    def testWiresIgnitionOverrideThroughToOutputs(self):
        """
        \\brief ignition_on=False 스냅샷만 제출해도(드라이버 명령 없음)
               actuatorAdapter/displayAdapter가 강제 RELEASE/OFF를 반영하는지
               검증한다(OVERRIDE 정책 배선이 빠지면 이 테스트는 실패해야 한다).
        \\technique 실제 컴포넌트 기반 (통합형 단위 테스트, SWR-020 조립 계약)
        \\testtype 긍정 (Positive)
        \\see UNIT-105 / FN-105, SWD-PH1 §5.9 사후조건, SWR-020
        """
        handle = buildSystem()
        handle.vehicleAdapter.submit({"timestamp_s": 0.0, "ignition_on": False})

        self.assertEqual(handle.actuatorAdapter.getLastApplied().left, LockState.RELEASE)
        self.assertEqual(handle.actuatorAdapter.getLastApplied().right, LockState.RELEASE)
        self.assertEqual(
            handle.displayAdapter.getLastShown(), (DisplayState.OFF, ReasonCode.IGNITION_OFF)
        )

    def testEachCallReturnsIndependentSystem(self):
        """
        \\brief buildSystem()을 두 번 호출하면 서로 독립된 인스턴스(상태를 공유하지
               않음)가 반환되는지 검증한다. (전역 싱글턴으로 바뀌어 상태가 공유되면
               이 테스트는 실패해야 한다)
        \\technique 오류추정 (숨은 전역 상태 공유 방지)
        \\testtype 부정 (Negative)
        \\see UNIT-105 / FN-105, SWD-PH1 §5.9
        """
        first = buildSystem()
        second = buildSystem()
        first.driverAdapter.submit({"side": "all", "action": "lock", "source": "avn"})
        first.vehicleAdapter.submit({"timestamp_s": 0.0, "ignition_on": True})

        self.assertIsNone(second.actuatorAdapter.getLastApplied())


if __name__ == "__main__":
    unittest.main()
