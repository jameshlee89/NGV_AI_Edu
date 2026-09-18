"""
\brief UNIT-000(공통 자료형) 단위 테스트 — SWD-PH1 §4, §6.2 `derive_display_state` 근거.
"""
import unittest

import _bootstrap  # noqa: F401  pylint: disable=unused-import

from src.core.types import LockState, DisplayState, deriveDisplayState


class TestDeriveDisplayState(unittest.TestCase):
    """UNIT-000 공통 헬퍼 deriveDisplayState의 4가지 완전 조합을 검증한다 (SWD-PH1 §6.2)."""

    def testReturnsLockedAllWhenBothLocked(self):
        """
        \\brief (LOCK, LOCK) 입력이 LOCKED_ALL을 반환하는지 검증한다.
               (조합표의 이 행이 삭제/변경되면 이 테스트는 실패해야 한다)
        \\technique 결정테이블 테스트 (SWD-PH1 §6.2, (LOCK,LOCK)→LOCKED_ALL 행)
        \\testtype 긍정 (Positive)
        \\see UNIT-000 / §6.2
        """
        self.assertEqual(
            deriveDisplayState(LockState.LOCK, LockState.LOCK), DisplayState.LOCKED_ALL
        )

    def testReturnsLockedLeftWhenOnlyLeftLocked(self):
        """
        \\brief (LOCK, RELEASE) 입력이 LOCKED_LEFT를 반환하는지 검증한다.
               (좌/우 판정이 뒤바뀌면 이 테스트는 실패해야 한다)
        \\technique 결정테이블 테스트 (SWD-PH1 §6.2, (LOCK,RELEASE)→LOCKED_LEFT 행)
        \\testtype 긍정 (Positive)
        \\see UNIT-000 / §6.2
        """
        self.assertEqual(
            deriveDisplayState(LockState.LOCK, LockState.RELEASE), DisplayState.LOCKED_LEFT
        )

    def testReturnsLockedRightWhenOnlyRightLocked(self):
        """
        \\brief (RELEASE, LOCK) 입력이 LOCKED_RIGHT를 반환하는지 검증한다.
               (좌/우 판정이 뒤바뀌면 이 테스트는 실패해야 한다)
        \\technique 결정테이블 테스트 (SWD-PH1 §6.2, (RELEASE,LOCK)→LOCKED_RIGHT 행)
        \\testtype 긍정 (Positive)
        \\see UNIT-000 / §6.2
        """
        self.assertEqual(
            deriveDisplayState(LockState.RELEASE, LockState.LOCK), DisplayState.LOCKED_RIGHT
        )

    def testReturnsReleasedWhenBothReleased(self):
        """
        \\brief (RELEASE, RELEASE) 입력이 RELEASED를 반환하는지 검증한다.
               (기본값 분기가 삭제되면 이 테스트는 실패해야 한다)
        \\technique 결정테이블 테스트 (SWD-PH1 §6.2, (RELEASE,RELEASE)→RELEASED 행)
        \\testtype 긍정 (Positive)
        \\see UNIT-000 / §6.2
        """
        self.assertEqual(
            deriveDisplayState(LockState.RELEASE, LockState.RELEASE), DisplayState.RELEASED
        )


if __name__ == "__main__":
    unittest.main()
