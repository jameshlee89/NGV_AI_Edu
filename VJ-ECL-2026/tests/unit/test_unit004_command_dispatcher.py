"""
\brief UNIT-004(CommandDispatcher) 단위 테스트 — FN-030/031/032, SWR-002, SWD-PH1 §5.2.
"""
import unittest

import _bootstrap  # noqa: F401  pylint: disable=unused-import

from src.core.types import Action, DriverCommand, Rejection, ReasonCode, Side, Source, ValidCommand
from src.core.command_dispatcher import CommandDispatcher
from src.core.command_validator import CommandValidator


class TestCommandDispatcher(unittest.TestCase):
    """dispatch/getCurrentCycleCommand/discardCurrentCycleCommand 왕복 동작을 검증한다."""

    def setUp(self):
        self.dispatcher = CommandDispatcher(CommandValidator())

    def testInitiallyHasNoStagedCommand(self):
        """
        \\brief 어떤 dispatch도 없었을 때 getCurrentCycleCommand()가 None을 반환하는지
               검증한다. (초기 staging 상태가 None이 아니면 이 테스트는 실패해야 한다)
        \\technique 경계값분석 (초기 상태 경계)
        \\testtype 긍정 (Positive)
        \\see UNIT-004 / FN-031, SWR-002
        """
        self.assertIsNone(self.dispatcher.getCurrentCycleCommand())

    def testDispatchStagesValidatedValidCommand(self):
        """
        \\brief 유효한 raw 명령을 dispatch하면 검증된 ValidCommand가 staging되어
               getCurrentCycleCommand()로 조회되는지 검증한다. (dispatch가 검증기를
               호출하지 않거나 값을 저장하지 않으면 이 테스트는 실패해야 한다)
        \\technique 실제 컴포넌트 기반 (실제 CommandValidator 사용)
        \\testtype 긍정 (Positive)
        \\see UNIT-004 / FN-030/031, SWR-002
        """
        self.dispatcher.dispatch(DriverCommand(side="left", action="lock", source="avn"))
        self.assertEqual(
            self.dispatcher.getCurrentCycleCommand(),
            ValidCommand(Side.LEFT, Action.LOCK, Source.AVN),
        )

    def testDispatchStagesRejectionForInvalidCommand(self):
        """
        \\brief 무효한 raw 명령을 dispatch하면 Rejection이 staging되는지 검증한다.
               (거절 결과가 무시되고 None이 staging되면 이 테스트는 실패해야 한다)
        \\technique 실제 컴포넌트 기반 (실제 CommandValidator 사용, 오류추정 입력)
        \\testtype 부정 (Negative)
        \\see UNIT-004 / FN-030/031, SWR-001(b)/002
        """
        self.dispatcher.dispatch(DriverCommand(side="unknown", action="lock", source="avn"))
        self.assertEqual(
            self.dispatcher.getCurrentCycleCommand(), Rejection(ReasonCode.INVALID_COMMAND)
        )

    def testGetCurrentCycleCommandDoesNotClearStagedValue(self):
        """
        \\brief getCurrentCycleCommand()를 두 번 호출해도 값이 그대로 유지되는지(부작용
               없음) 검증한다. (조회가 값을 지우면 이 테스트는 실패해야 한다)
        \\technique 실제 컴포넌트 기반 (반복 호출)
        \\testtype 긍정 (Positive)
        \\see UNIT-004 / FN-031, SWD-PH1 §5.2 "부작용 없음"
        """
        self.dispatcher.dispatch(DriverCommand(side="all", action="unlock", source="voice"))
        first = self.dispatcher.getCurrentCycleCommand()
        second = self.dispatcher.getCurrentCycleCommand()
        self.assertEqual(first, second)

    def testDiscardClearsStagedCommand(self):
        """
        \\brief discardCurrentCycleCommand() 호출 후 getCurrentCycleCommand()가 None을
               반환하는지 검증한다. (폐기 로직이 제거되면 이 테스트는 실패해야 한다)
        \\technique 상태전이 테스트 (staged -> discarded)
        \\testtype 긍정 (Positive)
        \\see UNIT-004 / FN-032, SWR-002/020(b)
        """
        self.dispatcher.dispatch(DriverCommand(side="left", action="lock", source="avn"))
        self.dispatcher.discardCurrentCycleCommand()
        self.assertIsNone(self.dispatcher.getCurrentCycleCommand())

    def testDispatchOverwritesPreviousStagedValueWithWarning(self):
        """
        \\brief 같은 주기에 dispatch가 2회 호출되면 마지막 값으로 덮어쓰고 WARNING
               로그를 남기는지 검증한다(SWR-PH1 가정2 위반 방어). (덮어쓰기 없이 첫
               값이 유지되거나 경고 로그가 없으면 이 테스트는 실패해야 한다)
        \\technique 오류추정 (가정 위반 입력 — 평가주기당 2회 이상 호출)
        \\testtype 부정 (Negative)
        \\see UNIT-004 / FN-030, SWD-PH1 §10.2
        """
        first = DriverCommand(side="left", action="lock", source="avn")
        second = DriverCommand(side="right", action="unlock", source="voice")
        with self.assertLogs("vjecl.core.command_dispatcher", level="WARNING"):
            self.dispatcher.dispatch(first)
            self.dispatcher.dispatch(second)
        self.assertEqual(
            self.dispatcher.getCurrentCycleCommand(),
            ValidCommand(Side.RIGHT, Action.UNLOCK, Source.VOICE),
        )

    def testDispatchTreatsAllFourSourcesEquallyWhenStaging(self):
        """
        \\brief source 값이 4채널 중 무엇이든 staging된 ValidCommand.source가 그대로
               보존되고 side/action 처리에 차별이 없는지 검증한다(SWR-002 동등 처리의
               디스패처 단 실증). (source에 따라 staging이 달라지거나 거절되면 이
               테스트는 실패해야 한다)
        \\technique 동등분할 (source 4채널 동등클래스 전수, SWR-002)
        \\testtype 긍정 (Positive)
        \\see UNIT-004 / FN-030, SWR-002
        """
        for source in (Source.PHYSICAL_BUTTON, Source.AVN, Source.VOICE, Source.MOBILE_APP):
            with self.subTest(source=source):
                dispatcher = CommandDispatcher(CommandValidator())
                dispatcher.dispatch(DriverCommand(side="left", action="lock", source=source.value))
                self.assertEqual(
                    dispatcher.getCurrentCycleCommand(),
                    ValidCommand(Side.LEFT, Action.LOCK, source),
                )


if __name__ == "__main__":
    unittest.main()
