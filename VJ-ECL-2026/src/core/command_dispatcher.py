"""
\brief UNIT-004 CommandDispatcher — 이번 평가주기 명령 1건의 보관/조회/폐기만 담당.

아키텍처 요소 대응: ARC-004. 상세설계 근거: SWD-PH1_SW 상세설계서.md §5.2(FN-030/031/032).
관련 요구사항: SWR-002. **SWR-002 정적 점검**: 이 구현은 `raw.source`/`ValidCommand.source`
값을 어떤 조건문에서도 참조하지 않는다(§5.2/§11.1 근거) — source는 CommandValidator가
반환한 값에 보존될 뿐, 이 클래스는 side/action/source를 구분하지 않고 동일하게 저장한다.
"""
import logging

from src.core.types import DriverCommand, Rejection, ValidCommand
from src.core.command_validator import CommandValidator

_logger = logging.getLogger("vjecl.core.command_dispatcher")


class CommandDispatcher:
    """\brief IF-INT-006 구현체 — dispatch/getCurrentCycleCommand/discard를 제공한다."""

    def __init__(self, validator: CommandValidator) -> None:
        """\brief 생성자 주입으로 CommandValidator를 받아 보관한다."""
        self._validator = validator
        self._staged: ValidCommand | Rejection | None = None

    def dispatch(self, raw: DriverCommand) -> None:
        """
        \\brief `raw`를 검증해 이번 평가주기의 staged 값으로 저장한다.

        \\param raw 검증 전 DriverCommand
        \\exception 발생하지 않음(내부 검증기가 이미 총함수, §5.1)

        이미 staged 값이 있었다면 새 값으로 덮어쓰고 `logging.WARNING`으로 SWR-PH1
        가정2(평가주기당 최대 1건) 위반 가능성을 기록한다(SWD-PH1 §10.2).
        """
        if self._staged is not None:
            _logger.warning(
                "같은 평가주기에 dispatch가 2회 이상 호출됨 (SWR-PH1 가정2 위반 가능성) — "
                "마지막 값으로 덮어씀"
            )
        self._staged = self._validator.validate(raw)

    def getCurrentCycleCommand(self) -> ValidCommand | Rejection | None:
        """
        \\brief 이번 주기 staged 값을 부작용 없이 조회한다.

        \\return staged 값(없으면 None)
        \\exception 발생하지 않음
        """
        return self._staged

    def discardCurrentCycleCommand(self) -> None:
        """
        \\brief 이번 주기 staged 값을 초기화한다(멱등).

        \\exception 발생하지 않음
        """
        self._staged = None
