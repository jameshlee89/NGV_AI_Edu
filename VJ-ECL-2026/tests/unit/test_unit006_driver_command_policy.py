"""
\brief UNIT-006(DriverCommandPolicy) 단위 테스트 — FN-050, SWR-004,
       SWD-PH1 §5.4/§6.2/§7.1 의사결정표(12+2행).
"""
import unittest

import _bootstrap  # noqa: F401  pylint: disable=unused-import

from src.core.types import (
    Action,
    DisplayState,
    DriverCommand,
    LockState,
    PolicyContext,
    PolicyDecision,
    ReasonCode,
    Side,
    VehicleSnapshot,
    deriveDisplayState,
)
from src.core.command_dispatcher import CommandDispatcher
from src.core.command_validator import CommandValidator
from src.core.lock_state_store import LockStateStore
from src.core.policies.driver_command_policy import DriverCommandPolicy


def _buildPolicy(preLeft: LockState, preRight: LockState):
    """테스트 헬퍼 — 사전상태를 세팅한 실제 LockStateStore/CommandDispatcher로 정책을 구성."""
    store = LockStateStore()
    store.write(preLeft, preRight)
    dispatcher = CommandDispatcher(CommandValidator())
    return DriverCommandPolicy(dispatcher, store), store, dispatcher


# SWR-004 §7.1 행 1~12 (side, action, preLeft, preRight, expectedLeft, expectedRight)
_DECISION_TABLE_ROWS = [
    (1, Side.LEFT, Action.LOCK, LockState.LOCK, LockState.LOCK, LockState.LOCK, LockState.LOCK),
    (2, Side.LEFT, Action.LOCK, LockState.RELEASE, LockState.RELEASE,
     LockState.LOCK, LockState.RELEASE),
    (3, Side.LEFT, Action.UNLOCK, LockState.LOCK, LockState.LOCK,
     LockState.RELEASE, LockState.LOCK),
    (4, Side.LEFT, Action.UNLOCK, LockState.RELEASE, LockState.RELEASE,
     LockState.RELEASE, LockState.RELEASE),
    (5, Side.RIGHT, Action.LOCK, LockState.LOCK, LockState.LOCK,
     LockState.LOCK, LockState.LOCK),
    (6, Side.RIGHT, Action.LOCK, LockState.RELEASE, LockState.RELEASE,
     LockState.RELEASE, LockState.LOCK),
    (7, Side.RIGHT, Action.UNLOCK, LockState.LOCK, LockState.LOCK,
     LockState.LOCK, LockState.RELEASE),
    (8, Side.RIGHT, Action.UNLOCK, LockState.RELEASE, LockState.RELEASE,
     LockState.RELEASE, LockState.RELEASE),
    (9, Side.ALL, Action.LOCK, LockState.LOCK, LockState.LOCK,
     LockState.LOCK, LockState.LOCK),
    (10, Side.ALL, Action.LOCK, LockState.RELEASE, LockState.RELEASE,
     LockState.LOCK, LockState.LOCK),
    (11, Side.ALL, Action.UNLOCK, LockState.LOCK, LockState.LOCK,
     LockState.RELEASE, LockState.RELEASE),
    (12, Side.ALL, Action.UNLOCK, LockState.RELEASE, LockState.RELEASE,
     LockState.RELEASE, LockState.RELEASE),
]


class TestDriverCommandPolicyDecisionTable(unittest.TestCase):
    """SWD-PH1 §7.1 의사결정표 12행(유효 명령)을 모두 검증한다."""

    def testAppliesAllTwelveValidCommandRows(self):
        """
        \\brief §7.1 행 1~12(3 side × 2 action × 2 사전상태) 각각에서 선택 출력만
               갱신되고 나머지는 사전상태를 유지하며 reason_code=NONE인지 검증한다.
               (side/action 분기나 미선택 출력 보존 로직이 깨지면 이 테스트는 실패해야
               한다)
        \\technique 결정테이블 테스트 (SWD-PH1 §7.1, 12행 전수)
        \\testtype 긍정 (Positive)
        \\see UNIT-006 / FN-050, SWR-004
        """
        for rowId, side, action, preLeft, preRight, expLeft, expRight in _DECISION_TABLE_ROWS:
            with self.subTest(row=rowId):
                policy, _, dispatcher = _buildPolicy(preLeft, preRight)
                dispatcher.dispatch(DriverCommand(side=side.value, action=action.value, source="avn"))
                context = PolicyContext(VehicleSnapshot(timestampS=0.0, ignitionOn=True))
                result = policy.evaluate(context)
                self.assertEqual(result.decision, PolicyDecision.PROPOSE)
                self.assertEqual(result.lockLeft, expLeft)
                self.assertEqual(result.lockRight, expRight)
                self.assertEqual(result.reasonCode, ReasonCode.NONE)
                self.assertEqual(result.stateLabel, deriveDisplayState(expLeft, expRight))


class TestDriverCommandPolicyNoCommand(unittest.TestCase):
    """SWD-PH1 §7.1 행 13(입력 없음)을 검증한다."""

    def testKeepsCurrentValuesWhenNoCommandStaged(self):
        """
        \\brief 이번 주기에 staged 명령이 없으면(getCurrentCycleCommand()가 None) 현재
               값을 그대로 유지하고 reason_code=NONE을 반환하는지 검증한다. (cmd is
               None 분기가 삭제되면 이 테스트는 실패해야 한다)
        \\technique 결정테이블 테스트 (SWD-PH1 §7.1 행13, 동등분할: cmd=None 클래스)
        \\testtype 긍정 (Positive)
        \\see UNIT-006 / FN-050, SWR-004 §7.1 행13
        """
        policy, _, _ = _buildPolicy(LockState.LOCK, LockState.RELEASE)
        context = PolicyContext(VehicleSnapshot(timestampS=0.0, ignitionOn=True))
        result = policy.evaluate(context)
        self.assertEqual(result.lockLeft, LockState.LOCK)
        self.assertEqual(result.lockRight, LockState.RELEASE)
        self.assertEqual(result.reasonCode, ReasonCode.NONE)
        self.assertEqual(result.stateLabel, DisplayState.LOCKED_LEFT)


class TestDriverCommandPolicyRejection(unittest.TestCase):
    """SWD-PH1 §7.1 행14(SWR-001b 거절)을 검증한다."""

    def testKeepsCurrentValuesAndFlagsInvalidCommandWhenRejected(self):
        """
        \\brief 이번 주기 명령이 Rejection이면 현재 값을 유지하고
               reason_code=INVALID_COMMAND를 반환하는지 검증한다. (Rejection 분기가
               삭제되면 이 테스트는 실패해야 한다)
        \\technique 결정테이블 테스트 (SWD-PH1 §7.1 행14, 오류추정: Rejection 입력)
        \\testtype 부정 (Negative)
        \\see UNIT-006 / FN-050, SWR-004 §7.1 행14, SWR-001(b)
        """
        policy, _, dispatcher = _buildPolicy(LockState.RELEASE, LockState.LOCK)
        dispatcher.dispatch(DriverCommand(side="unknown", action="lock", source="avn"))
        context = PolicyContext(VehicleSnapshot(timestampS=0.0, ignitionOn=True))
        result = policy.evaluate(context)
        self.assertEqual(result.lockLeft, LockState.RELEASE)
        self.assertEqual(result.lockRight, LockState.LOCK)
        self.assertEqual(result.reasonCode, ReasonCode.INVALID_COMMAND)


if __name__ == "__main__":
    unittest.main()
