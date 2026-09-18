"""
\brief UNIT-008(PolicyPort 등 포트 정의) 단위 테스트 — SWD-PH1 §4.6.
"""
import unittest

import _bootstrap  # noqa: F401  pylint: disable=unused-import

from src.core.types import (
    AsilLevel,
    DisplayState,
    LockState,
    PolicyCategory,
    PolicyContext,
    PolicyDecision,
    PolicyResult,
    ReasonCode,
    VehicleSnapshot,
)
from src.core.policy_port import ActuatorPort, DisplayPort, PolicyPort


class _ConformingPolicy:
    """테스트 전용 스텁 — PolicyPort의 모든 속성/메서드 형태를 구조적으로 만족한다."""

    category = PolicyCategory.BASE
    asilLevel = AsilLevel.QM
    priority = 1

    def evaluate(self, context: PolicyContext) -> PolicyResult:
        return PolicyResult(decision=PolicyDecision.PASS)


class _NonConformingPolicy:
    """테스트 전용 스텁 — evaluate 메서드가 없어 PolicyPort를 만족하지 않는다."""

    category = PolicyCategory.BASE
    asilLevel = AsilLevel.QM
    priority = 1


class _ConformingActuator:
    """테스트 전용 스텁 — ActuatorPort(apply)를 구조적으로 만족한다."""

    def apply(self, lockLeft: LockState, lockRight: LockState) -> None:
        return None


class _ConformingDisplay:
    """테스트 전용 스텁 — DisplayPort(show)를 구조적으로 만족한다."""

    def show(self, state: DisplayState, reasonCode: ReasonCode) -> None:
        return None


class TestPolicyPortConformance(unittest.TestCase):
    """PolicyPort/ActuatorPort/DisplayPort 구조적 서브타이핑(LSP) 판정을 검증한다."""

    def testConformingPolicyIsRecognizedAsPolicyPort(self):
        """
        \\brief evaluate/category/asilLevel/priority를 모두 갖춘 스텁이 PolicyPort로
               인식되는지 검증한다. (PolicyPort의 @runtime_checkable 선언이나 시그니처
               정의가 깨지면 이 테스트는 실패해야 한다)
        \\technique 실제 컴포넌트 기반 (구조적 서브타이핑, LSP 검증)
        \\testtype 긍정 (Positive)
        \\see UNIT-008 / SWD-PH1 §4.6
        """
        self.assertIsInstance(_ConformingPolicy(), PolicyPort)

    def testNonConformingPolicyIsNotRecognizedAsPolicyPort(self):
        """
        \\brief evaluate 메서드가 없는 스텁은 PolicyPort로 인식되지 않아야 함을 검증한다.
               (PolicyPort가 아무 클래스나 통과시키도록 잘못 넓어지면 이 테스트는
               실패해야 한다)
        \\technique 오류추정 (필수 메서드 누락)
        \\testtype 부정 (Negative)
        \\see UNIT-008 / SWD-PH1 §4.6
        """
        self.assertNotIsInstance(_NonConformingPolicy(), PolicyPort)

    def testConformingActuatorIsRecognizedAsActuatorPort(self):
        """
        \\brief apply(lockLeft, lockRight)를 갖춘 스텁이 ActuatorPort로 인식되는지 검증한다.
               (ActuatorPort 정의가 삭제/오타나면 이 테스트는 실패해야 한다)
        \\technique 실제 컴포넌트 기반 (구조적 서브타이핑)
        \\testtype 긍정 (Positive)
        \\see UNIT-008 / SWD-PH1 §4.6
        """
        self.assertIsInstance(_ConformingActuator(), ActuatorPort)

    def testConformingDisplayIsRecognizedAsDisplayPort(self):
        """
        \\brief show(state, reasonCode)를 갖춘 스텁이 DisplayPort로 인식되는지 검증한다.
               (DisplayPort 정의가 삭제/오타나면 이 테스트는 실패해야 한다)
        \\technique 실제 컴포넌트 기반 (구조적 서브타이핑)
        \\testtype 긍정 (Positive)
        \\see UNIT-008 / SWD-PH1 §4.6
        """
        self.assertIsInstance(_ConformingDisplay(), DisplayPort)


if __name__ == "__main__":
    unittest.main()
