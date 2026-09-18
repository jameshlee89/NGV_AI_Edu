"""
\brief UNIT-104(DisplayOutputTestAdapter) 단위 테스트 — FN-104, SWD-PH1 §5.8.
"""
import unittest

import _bootstrap  # noqa: F401  pylint: disable=unused-import

from src.core.types import DisplayState, ReasonCode
from src.adapters.pcsil.display_output_test_adapter import DisplayOutputTestAdapter


class TestDisplayOutputTestAdapter(unittest.TestCase):
    """show/getLastShown 왕복 동작을 검증한다 (IF-INT-004 구현 + 시험용 확장)."""

    def setUp(self):
        self.adapter = DisplayOutputTestAdapter()

    def testGetLastShownIsNoneBeforeAnyShow(self):
        """
        \\brief show()가 한 번도 호출되지 않았을 때 getLastShown()이 None을 반환하는지
               검증한다. (초기값이 임의의 튜플이면 이 테스트는 실패해야 한다)
        \\technique 경계값분석 (초기 상태 경계)
        \\testtype 긍정 (Positive)
        \\see UNIT-104 / FN-104, SWD-PH1 §5.8
        """
        self.assertIsNone(self.adapter.getLastShown())

    def testGetLastShownReturnsLastShownTuple(self):
        """
        \\brief show(LOCKED_LEFT, NONE) 호출 후 getLastShown()이 (state, reasonCode)
               튜플을 반환하는지 검증한다. (show가 상태를 저장하지 않으면 이 테스트는
               실패해야 한다)
        \\technique 실제 컴포넌트 기반 (왕복 검증)
        \\testtype 긍정 (Positive)
        \\see UNIT-104 / FN-104, SWR-001(b)/020
        """
        self.adapter.show(DisplayState.LOCKED_LEFT, ReasonCode.NONE)
        self.assertEqual(
            self.adapter.getLastShown(), (DisplayState.LOCKED_LEFT, ReasonCode.NONE)
        )

    def testShowOverwritesPreviousValue(self):
        """
        \\brief 두 번째 show가 첫 번째 show 값을 완전히 덮어쓰는지 검증한다.
               (누적/병합되면 이 테스트는 실패해야 한다)
        \\technique 상태전이 테스트 (연속 show)
        \\testtype 긍정 (Positive)
        \\see UNIT-104 / FN-104
        """
        self.adapter.show(DisplayState.LOCKED_ALL, ReasonCode.NONE)
        self.adapter.show(DisplayState.OFF, ReasonCode.IGNITION_OFF)
        self.assertEqual(self.adapter.getLastShown(), (DisplayState.OFF, ReasonCode.IGNITION_OFF))


if __name__ == "__main__":
    unittest.main()
