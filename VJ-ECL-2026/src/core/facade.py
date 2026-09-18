"""
\brief UNIT-001 EvaluationCycleFacade — 구동 어댑터에 노출되는 단일 진입점.

아키텍처 요소 대응: ARC-001. 상세설계 근거: SWD-PH1_SW 상세설계서.md §5.7(FN-001/002).
관련 요구사항: SWR-001, SWR-002, SWR-004, SWR-020(위임 대상 로직 근거).
"""
from src.core.types import DriverCommand, EvaluationResult, VehicleSnapshot
from src.core.command_dispatcher import CommandDispatcher
from src.core.policy_chain_executor import PolicyChainExecutor


class EvaluationCycleFacade:
    """\brief IF-INT-001/002 구현체 — Driver 명령 위임, Vehicle 스냅샷 평가 트리거."""

    def __init__(self, dispatcher: CommandDispatcher, executor: PolicyChainExecutor) -> None:
        """\brief 생성자 주입으로 CommandDispatcher/PolicyChainExecutor를 받아 보관한다."""
        self._dispatcher = dispatcher
        self._executor = executor

    def submitDriverCommand(self, raw: DriverCommand) -> None:
        """
        \\brief `raw` Driver 명령을 CommandDispatcher.dispatch()에 그대로 위임한다.

        \\param raw 검증 전 DriverCommand
        \\exception 발생하지 않음(하위 계약이 이미 총함수)
        """
        self._dispatcher.dispatch(raw)

    def submitVehicleSnapshot(self, snapshot: VehicleSnapshot) -> EvaluationResult:
        """
        \\brief `snapshot`을 PolicyChainExecutor.evaluate()에 위임하고 결과를 반환한다.

        \\param snapshot 이번 평가주기의 VehicleSnapshot
        \\return PolicyChainExecutor.evaluate()의 반환값 그대로
        \\exception 발생하지 않음(FN-010이 이미 총함수)
        """
        return self._executor.evaluate(snapshot)
