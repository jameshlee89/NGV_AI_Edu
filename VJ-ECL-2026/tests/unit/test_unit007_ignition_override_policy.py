"""
\brief UNIT-007(IgnitionOverridePolicy) 단위 테스트 — FN-060/061, SWR-020,
       SWD-PH1 §5.5/§6.3/§7.2 의사결정표(3행)/§8.2 상태전이(4케이스).
"""
import unittest

import _bootstrap  # noqa: F401  pylint: disable=unused-import

from src.core.types import (
    DisplayState,
    IgnitionState,
    LockState,
    PolicyContext,
    PolicyDecision,
    ReasonCode,
    VehicleSnapshot,
)
from src.core.lock_state_store import LockStateStore
from src.core.policies.ignition_override_policy import IgnitionOverridePolicy, classifyIgnition


class _SpyLockStateStore(LockStateStore):
    """테스트 전용 스파이 — readCurrent() 호출 횟수를 기록해 의존 계약 이행을 검증한다."""

    def __init__(self):
        super().__init__()
        self.readCurrentCallCount = 0

    def readCurrent(self):
        self.readCurrentCallCount += 1
        return super().readCurrent()


class TestClassifyIgnition(unittest.TestCase):
    """FN-061 classifyIgnition의 총함수 판정을 검증한다 (SWR-020(b))."""

    def testClassifiesTrueAsOn(self):
        """
        \\brief bool True 입력이 IgnitionState.ON으로 분류되는지 검증한다.
               (True/False 판정 순서가 뒤바뀌면 이 테스트는 실패해야 한다)
        \\technique 동등분할 (유효 True 클래스)
        \\testtype 긍정 (Positive)
        \\see UNIT-007 / FN-061, SWR-020
        """
        self.assertEqual(classifyIgnition(True), IgnitionState.ON)

    def testClassifiesFalseAsOff(self):
        """
        \\brief bool False 입력이 IgnitionState.OFF로 분류되는지 검증한다.
               (False가 INVALID로 잘못 분류되면 이 테스트는 실패해야 한다)
        \\technique 동등분할 (유효 False 클래스)
        \\testtype 긍정 (Positive)
        \\see UNIT-007 / FN-061, SWR-020
        """
        self.assertEqual(classifyIgnition(False), IgnitionState.OFF)

    def testClassifiesNonBooleanValuesAsInvalid(self):
        """
        \\brief None/문자열/정수 등 bool이 아닌 모든 값이 IgnitionState.INVALID로
               분류되는지 검증한다(SWR-020(b) 안전측 처리). (형식 오류 값이 조용히
               ON/OFF로 처리되면 이 테스트는 실패해야 한다)
        \\technique 오류추정 (형식 오류/누락 입력 전수)
        \\testtype 부정 (Negative)
        \\see UNIT-007 / FN-061, SWR-020(b)
        """
        for raw in (None, "TRUE", 1, 0, 1.0):
            with self.subTest(raw=raw):
                self.assertEqual(classifyIgnition(raw), IgnitionState.INVALID)


class TestIgnitionOverridePolicyEvaluate(unittest.TestCase):
    """FN-060 evaluate의 §7.2 의사결정표 3행을 검증한다."""

    def _buildPolicy(self, preLeft=LockState.LOCK, preRight=LockState.LOCK):
        store = _SpyLockStateStore()
        store.write(preLeft, preRight)
        return IgnitionOverridePolicy(store), store

    def testPassesWhenIgnitionOn(self):
        """
        \\brief ignition_on=True이면 PolicyResult(decision=PASS)만 반환하는지 검증한다.
               (ON 판정 시에도 강제 RELEASE가 발생하면 이 테스트는 실패해야 한다)
        \\technique 결정테이블 테스트 (SWD-PH1 §7.2 행1)
        \\testtype 긍정 (Positive)
        \\see UNIT-007 / FN-060, SWR-020, §7.2 행1
        """
        policy, _ = self._buildPolicy()
        context = PolicyContext(VehicleSnapshot(timestampS=0.0, ignitionOn=True))
        result = policy.evaluate(context)
        self.assertEqual(result.decision, PolicyDecision.PASS)
        self.assertIsNone(result.lockLeft)
        self.assertIsNone(result.lockRight)
        self.assertIsNone(result.reasonCode)
        self.assertIsNone(result.stateLabel)

    def testForcesReleaseWhenIgnitionOff(self):
        """
        \\brief ignition_on=False이면 OVERRIDE_FINAL + RELEASE/RELEASE +
               IGNITION_OFF + OFF를 반환하는지 검증한다(직전 값이 LOCK/LOCK이었어도
               무조건 RELEASE). (강제 RELEASE 로직이 삭제되면 이 테스트는 실패해야 한다)
        \\technique 결정테이블 테스트 (SWD-PH1 §7.2 행2, SWR-020 상태전이 케이스1)
        \\testtype 긍정 (Positive)
        \\see UNIT-007 / FN-060, SWR-020, §7.2 행2, §8.2 케이스1
        """
        policy, store = self._buildPolicy(LockState.LOCK, LockState.LOCK)
        context = PolicyContext(VehicleSnapshot(timestampS=1.0, ignitionOn=False))
        result = policy.evaluate(context)
        self.assertEqual(result.decision, PolicyDecision.OVERRIDE_FINAL)
        self.assertEqual(result.lockLeft, LockState.RELEASE)
        self.assertEqual(result.lockRight, LockState.RELEASE)
        self.assertEqual(result.reasonCode, ReasonCode.IGNITION_OFF)
        self.assertEqual(result.stateLabel, DisplayState.OFF)
        self.assertGreaterEqual(store.readCurrentCallCount, 1)

    def testForcesReleaseWhenIgnitionInvalid(self):
        """
        \\brief ignition_on이 형식 오류(예: None)이면 False와 동일하게 강제 RELEASE로
               처리하는지 검증한다(SWR-020(b)). (INVALID를 PASS로 잘못 처리하면 이
               테스트는 실패해야 한다)
        \\technique 결정테이블 테스트 (SWD-PH1 §7.2 행3, SWR-020 상태전이 케이스4)
        \\testtype 부정 (Negative)
        \\see UNIT-007 / FN-060, SWR-020(b), §7.2 행3, §8.2 케이스4
        """
        policy, _ = self._buildPolicy(LockState.RELEASE, LockState.RELEASE)
        context = PolicyContext(VehicleSnapshot(timestampS=2.0, ignitionOn=None))
        result = policy.evaluate(context)
        self.assertEqual(result.decision, PolicyDecision.OVERRIDE_FINAL)
        self.assertEqual(result.lockLeft, LockState.RELEASE)
        self.assertEqual(result.lockRight, LockState.RELEASE)
        self.assertEqual(result.reasonCode, ReasonCode.IGNITION_OFF)

    def testReReleaseIsMaintainedAfterReturningToOn(self):
        """
        \\brief 직전 주기까지 OFF로 인해 (RELEASE,RELEASE)가 기록된 상태에서
               ignition_on이 다시 True로 전환되면, evaluate는 PASS를 반환하고
               (읽은 현재값을 그대로 두므로) 값 복원을 시도하지 않는지 검증한다
               (SWR-020(c) 재전환 유지, §8.2 케이스3). (PASS 시에도 값을 강제로
               복원하는 코드가 추가되면 이 테스트는 실패해야 한다 — 이 정책은 값을
               쓰지 않으므로 store는 그대로 RELEASE/RELEASE를 유지해야 한다)
        \\technique 상태전이 테스트 (SWD-PH1 §8.2 케이스3, OFF→ACTIVE 재전환)
        \\testtype 긍정 (Positive)
        \\see UNIT-007 / FN-060, SWR-020(c), §8.2 케이스3
        """
        policy, store = self._buildPolicy(LockState.RELEASE, LockState.RELEASE)
        context = PolicyContext(VehicleSnapshot(timestampS=3.0, ignitionOn=True))
        result = policy.evaluate(context)
        self.assertEqual(result.decision, PolicyDecision.PASS)
        self.assertEqual(store.readCurrent(), store.readCurrent())  # 값 변경 없음(부작용 없음)
        self.assertEqual(store.readCurrent().left, LockState.RELEASE)
        self.assertEqual(store.readCurrent().right, LockState.RELEASE)


if __name__ == "__main__":
    unittest.main()
