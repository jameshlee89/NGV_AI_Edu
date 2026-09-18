"""
\brief UNIT-006 DriverCommandPolicy — side 선택 출력 계산(BASE 정책)만 담당.

아키텍처 요소 대응: ARC-006. 상세설계 근거: SWD-PH1_SW 상세설계서.md §5.4(FN-050),
§6.2(의사코드), §7.1(정책 의사결정표, 12+2행). 관련 요구사항: SWR-004.
"""
from src.core.types import (
    Action,
    AsilLevel,
    LockState,
    PolicyCategory,
    PolicyContext,
    PolicyDecision,
    PolicyResult,
    ReasonCode,
    Rejection,
    Side,
    ValidCommand,
    deriveDisplayState,
)
from src.core.command_dispatcher import CommandDispatcher
from src.core.lock_state_store import LockStateStore


class DriverCommandPolicy:
    """\brief IF-INT-008(BASE) 구현체 — category=BASE, asilLevel=QM, priority=1 (SWR-004)."""

    category = PolicyCategory.BASE
    asilLevel = AsilLevel.QM
    priority = 1

    def __init__(self, dispatcher: CommandDispatcher, store: LockStateStore) -> None:
        """\brief 생성자 주입으로 CommandDispatcher/LockStateStore를 받아 보관한다."""
        self._dispatcher = dispatcher
        self._store = store

    def evaluate(self, context: PolicyContext) -> PolicyResult:
        """
        \\brief 이번 주기 명령의 side/action에 따라 선택 출력만 갱신한다.

        \\param context 정책 평가 컨텍스트(이 정책은 snapshot을 직접 사용하지 않음)
        \\return PolicyResult(decision=PROPOSE, ...) — §7.1 의사결정표 참고
        \\exception 발생하지 않음(총함수)

        상세설계 근거: UNIT-006 / FN-050 (SWD-PH1 §5.4, §6.2, §7.1).
        """
        del context  # 이 BASE 정책은 ignition 판정을 하지 않는다(§5.4 근거)
        current = self._store.readCurrent()
        cmd = self._dispatcher.getCurrentCycleCommand()

        if cmd is None:
            newLeft, newRight, reason = current.left, current.right, ReasonCode.NONE
        elif isinstance(cmd, Rejection):
            newLeft, newRight, reason = current.left, current.right, ReasonCode.INVALID_COMMAND
        else:
            newLeft, newRight, reason = self._applyValidCommand(cmd, current)

        stateLabel = deriveDisplayState(newLeft, newRight)
        return PolicyResult(PolicyDecision.PROPOSE, newLeft, newRight, reason, stateLabel)

    @staticmethod
    def _applyValidCommand(cmd: ValidCommand, current):
        """\brief 유효 명령의 side/action을 적용해 (newLeft, newRight, reason)을 계산."""
        target = LockState.LOCK if cmd.action == Action.LOCK else LockState.RELEASE
        if cmd.side == Side.LEFT:
            newLeft, newRight = target, current.right
        elif cmd.side == Side.RIGHT:
            newLeft, newRight = current.left, target
        else:  # Side.ALL
            newLeft, newRight = target, target
        return newLeft, newRight, ReasonCode.NONE
