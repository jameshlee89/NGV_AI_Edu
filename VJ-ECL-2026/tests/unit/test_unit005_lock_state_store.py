"""
\brief UNIT-005(LockStateStore) 단위 테스트 — FN-040/041, SWR-004/020, SWD-PH1 §5.3.
"""
import unittest

import _bootstrap  # noqa: F401  pylint: disable=unused-import

from src.core.types import LockPair, LockState
from src.core.lock_state_store import LockStateStore


class TestLockStateStore(unittest.TestCase):
    """readCurrent/write 왕복 동작과 초기값·타입 방어를 검증한다."""

    def setUp(self):
        self.store = LockStateStore()

    def testInitialValueIsReleaseRelease(self):
        """
        \\brief 최초 상태(어떤 write도 없었을 때) readCurrent()가 (RELEASE, RELEASE)를
               반환하는지 검증한다. (초기값이 바뀌면 이 테스트는 실패해야 한다)
        \\technique 경계값분석 (초기 상태 경계)
        \\testtype 긍정 (Positive)
        \\see UNIT-005 / FN-040, SWR-PH1 §8 가정3
        """
        self.assertEqual(self.store.readCurrent(), LockPair(LockState.RELEASE, LockState.RELEASE))

    def testReadReturnsLastWrittenPair(self):
        """
        \\brief write(LOCK, RELEASE) 이후 readCurrent()가 그 값을 그대로 반환하는지
               검증한다. (write가 상태를 갱신하지 않으면 이 테스트는 실패해야 한다)
        \\technique 실제 컴포넌트 기반 (왕복 검증)
        \\testtype 긍정 (Positive)
        \\see UNIT-005 / FN-041, SWR-004/020
        """
        self.store.write(LockState.LOCK, LockState.RELEASE)
        self.assertEqual(self.store.readCurrent(), LockPair(LockState.LOCK, LockState.RELEASE))

    def testWriteOverwritesPreviousValue(self):
        """
        \\brief 두 번째 write가 첫 번째 write 값을 완전히 덮어쓰는지 검증한다.
               (이전 값과 병합/누적되면 이 테스트는 실패해야 한다)
        \\technique 상태전이 테스트 (연속 write)
        \\testtype 긍정 (Positive)
        \\see UNIT-005 / FN-041
        """
        self.store.write(LockState.LOCK, LockState.LOCK)
        self.store.write(LockState.RELEASE, LockState.RELEASE)
        self.assertEqual(
            self.store.readCurrent(), LockPair(LockState.RELEASE, LockState.RELEASE)
        )

    def testWriteRejectsNonLockStateLeft(self):
        """
        \\brief left 인자가 LockState 인스턴스가 아니면 TypeError를 던지는지 검증한다
               (내부 신뢰 경계 위반, 프로그래밍 오류로 즉시 실패). (타입 방어가 제거되면
               이 테스트는 실패해야 한다)
        \\technique 오류추정 (사전조건 위반 — 내부 신뢰 경계)
        \\testtype 부정 (Negative)
        \\see UNIT-005 / FN-041, SWD-PH1 §10.3
        """
        with self.assertRaises(TypeError):
            self.store.write("LOCK", LockState.RELEASE)

    def testWriteRejectsNonLockStateRight(self):
        """
        \\brief right 인자가 LockState 인스턴스가 아니면 TypeError를 던지는지 검증한다.
               (right 인자에 대한 타입 방어가 누락되면 이 테스트는 실패해야 한다)
        \\technique 오류추정 (사전조건 위반 — 내부 신뢰 경계)
        \\testtype 부정 (Negative)
        \\see UNIT-005 / FN-041, SWD-PH1 §10.3
        """
        with self.assertRaises(TypeError):
            self.store.write(LockState.LOCK, None)


if __name__ == "__main__":
    unittest.main()
