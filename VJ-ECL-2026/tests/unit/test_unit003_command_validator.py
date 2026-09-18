"""
\brief UNIT-003(CommandValidator) 단위 테스트 — FN-020, SWR-001, SWD-PH1 §5.1/§6.1.
"""
import unittest

import _bootstrap  # noqa: F401  pylint: disable=unused-import

from src.core.types import Action, DriverCommand, Rejection, ReasonCode, Side, Source, ValidCommand
from src.core.command_validator import CommandValidator


class TestCommandValidatorValidInputs(unittest.TestCase):
    """유효한 DriverCommand 조합에 대해 ValidCommand를 반환하는지 검증한다 (SWR-001a)."""

    def setUp(self):
        self.validator = CommandValidator()

    def testAcceptsEachValidSide(self):
        """
        \\brief side가 left/right/all 각각일 때 모두 ValidCommand로 판정되는지 검증한다.
               (Side enum 소속 판정 분기가 깨지면 이 테스트는 실패해야 한다)
        \\technique 동등분할 (side 유효 클래스 3값 전수)
        \\testtype 긍정 (Positive)
        \\see UNIT-003 / FN-020, SWR-001
        """
        for side in (Side.LEFT, Side.RIGHT, Side.ALL):
            with self.subTest(side=side):
                raw = DriverCommand(side=side.value, action="lock", source="avn")
                result = self.validator.validate(raw)
                self.assertEqual(result, ValidCommand(side, Action.LOCK, Source.AVN))

    def testAcceptsEachValidAction(self):
        """
        \\brief action이 lock/unlock 각각일 때 모두 ValidCommand로 판정되는지 검증한다.
               (Action enum 소속 판정 분기가 깨지면 이 테스트는 실패해야 한다)
        \\technique 동등분할 (action 유효 클래스 2값 전수)
        \\testtype 긍정 (Positive)
        \\see UNIT-003 / FN-020, SWR-001
        """
        for action in (Action.LOCK, Action.UNLOCK):
            with self.subTest(action=action):
                raw = DriverCommand(side="left", action=action.value, source="avn")
                result = self.validator.validate(raw)
                self.assertEqual(result, ValidCommand(Side.LEFT, action, Source.AVN))

    def testAcceptsEachValidSource(self):
        """
        \\brief source가 4개 채널 각각일 때 모두 ValidCommand로 판정되는지 검증한다.
               (Source enum 소속 판정 분기가 깨지면 이 테스트는 실패해야 한다)
        \\technique 동등분할 (source 유효 클래스 4값 전수, SWR-002 근거)
        \\testtype 긍정 (Positive)
        \\see UNIT-003 / FN-020, SWR-001/002
        """
        for source in (Source.PHYSICAL_BUTTON, Source.AVN, Source.VOICE, Source.MOBILE_APP):
            with self.subTest(source=source):
                raw = DriverCommand(side="left", action="lock", source=source.value)
                result = self.validator.validate(raw)
                self.assertEqual(result, ValidCommand(Side.LEFT, Action.LOCK, source))


class TestCommandValidatorRejections(unittest.TestCase):
    """무효 입력에 대해 Rejection(INVALID_COMMAND)을 반환하는지 검증한다 (SWR-001b)."""

    def setUp(self):
        self.validator = CommandValidator()

    def testRejectsWhenSideIsMissing(self):
        """
        \\brief side 필드가 누락(None)이면 Rejection(INVALID_COMMAND)을 반환하는지 검증한다.
               (누락 필드 검사가 제거되면 이 테스트는 실패해야 한다)
        \\technique 오류추정 (필드 누락)
        \\testtype 부정 (Negative)
        \\see UNIT-003 / FN-020, SWR-001(b)
        """
        raw = DriverCommand(side=None, action="lock", source="avn")
        self.assertEqual(self.validator.validate(raw), Rejection(ReasonCode.INVALID_COMMAND))

    def testRejectsWhenActionIsUnregisteredEnum(self):
        """
        \\brief action이 정의되지 않은 enum 값이면 Rejection(INVALID_COMMAND)을 반환하는지
               검증한다. (미등록 enum 거절 로직이 제거되면 이 테스트는 실패해야 한다)
        \\technique 오류추정 (미등록 enum 값)
        \\testtype 부정 (Negative)
        \\see UNIT-003 / FN-020, SWR-001(b)
        """
        raw = DriverCommand(side="left", action="toggle", source="avn")
        self.assertEqual(self.validator.validate(raw), Rejection(ReasonCode.INVALID_COMMAND))

    def testRejectsWhenSourceHasWrongFormat(self):
        """
        \\brief source가 형식 오류(정수 등 문자열이 아닌 값)이면 Rejection을 반환하는지
               검증한다. (형식 오류 방어가 제거되면 이 테스트는 실패해야 한다)
        \\technique 경계값분석 (예상 타입 경계를 벗어난 입력)
        \\testtype 부정 (Negative)
        \\see UNIT-003 / FN-020, SWR-001(b)
        """
        raw = DriverCommand(side="left", action="lock", source=123)
        self.assertEqual(self.validator.validate(raw), Rejection(ReasonCode.INVALID_COMMAND))

    def testRejectsWhenAllFieldsMissing(self):
        """
        \\brief 세 필드가 모두 누락되면 Rejection(INVALID_COMMAND)을 반환하는지 검증한다.
               (기본 DriverCommand()가 우연히 통과 처리되면 이 테스트는 실패해야 한다)
        \\technique 경계값분석 (완전 누락 — 최소 입력 경계)
        \\testtype 부정 (Negative)
        \\see UNIT-003 / FN-020, SWR-001(b)
        """
        self.assertEqual(
            self.validator.validate(DriverCommand()), Rejection(ReasonCode.INVALID_COMMAND)
        )

    def testRejectsWhenRawIsNotDriverCommandInstance(self):
        """
        \\brief raw가 DriverCommand 인스턴스가 아니면(예: dict) Rejection을 반환하는지
               검증한다. (총함수 방어 분기가 제거되면 이 테스트는 실패해야 한다)
        \\technique 오류추정 (호출자 계약 위반에 대한 방어적 완화, SWD-PH1 §10.1)
        \\testtype 부정 (Negative)
        \\see UNIT-003 / FN-020, SWD-PH1 §5.1 사전조건
        """
        self.assertEqual(
            self.validator.validate({"side": "left", "action": "lock", "source": "avn"}),
            Rejection(ReasonCode.INVALID_COMMAND),
        )

    def testRejectsWithoutRaisingException(self):
        """
        \\brief None을 입력해도 예외를 던지지 않고 Rejection 값을 반환하는지 검증한다
               (총함수 계약). (validate가 예외를 던지도록 바뀌면 이 테스트는 실패해야 한다)
        \\technique 오류추정 (None 입력, 총함수 계약 검증)
        \\testtype 부정 (Negative)
        \\see UNIT-003 / FN-020, SWD-PH1 §5.1 "사전조건 없음(총함수)"
        """
        try:
            result = self.validator.validate(None)
        except Exception as exc:  # pylint: disable=broad-except
            self.fail(f"validate(None)가 예외를 던짐: {exc!r}")
        self.assertEqual(result, Rejection(ReasonCode.INVALID_COMMAND))


if __name__ == "__main__":
    unittest.main()
