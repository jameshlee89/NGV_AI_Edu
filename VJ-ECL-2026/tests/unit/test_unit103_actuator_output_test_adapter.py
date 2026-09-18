"""
\brief UNIT-103(ActuatorOutputTestAdapter) 단위 테스트 — FN-103, SWD-PH1 §5.8.
"""
import unittest

import _bootstrap  # noqa: F401  pylint: disable=unused-import

from src.core.types import LockPair, LockState
from src.adapters.pcsil.actuator_output_test_adapter import ActuatorOutputTestAdapter


class TestActuatorOutputTestAdapter(unittest.TestCase):
    """apply/getLastApplied 왕복 동작을 검증한다 (IF-INT-003 구현 + 시험용 확장)."""

    def setUp(self):
        self.adapter = ActuatorOutputTestAdapter()

    def testGetLastAppliedIsNoneBeforeAnyApply(self):
        """
        \\brief apply()가 한 번도 호출되지 않았을 때 getLastApplied()가 None을
               반환하는지 검증한다. (초기값이 임의의 LockPair면 이 테스트는 실패해야
               한다)
        \\technique 경계값분석 (초기 상태 경계)
        \\testtype 긍정 (Positive)
        \\see UNIT-103 / FN-103, SWD-PH1 §5.8
        """
        self.assertIsNone(self.adapter.getLastApplied())

    def testGetLastAppliedReturnsLastAppliedPair(self):
        """
        \\brief apply(LOCK, RELEASE) 호출 후 getLastApplied()가 그 값을 LockPair로
               반환하는지 검증한다. (apply가 상태를 저장하지 않으면 이 테스트는
               실패해야 한다)
        \\technique 실제 컴포넌트 기반 (왕복 검증)
        \\testtype 긍정 (Positive)
        \\see UNIT-103 / FN-103, SWR-004/020
        """
        self.adapter.apply(LockState.LOCK, LockState.RELEASE)
        self.assertEqual(self.adapter.getLastApplied(), LockPair(LockState.LOCK, LockState.RELEASE))

    def testApplyOverwritesPreviousValue(self):
        """
        \\brief 두 번째 apply가 첫 번째 apply 값을 완전히 덮어쓰는지 검증한다.
               (누적/병합되면 이 테스트는 실패해야 한다)
        \\technique 상태전이 테스트 (연속 apply)
        \\testtype 긍정 (Positive)
        \\see UNIT-103 / FN-103
        """
        self.adapter.apply(LockState.LOCK, LockState.LOCK)
        self.adapter.apply(LockState.RELEASE, LockState.RELEASE)
        self.assertEqual(
            self.adapter.getLastApplied(), LockPair(LockState.RELEASE, LockState.RELEASE)
        )


if __name__ == "__main__":
    unittest.main()
